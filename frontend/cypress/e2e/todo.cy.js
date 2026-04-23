describe("Todo Item Creation and Management", () => {
  let userId;
  let name;
  let email;
  let taskId;

  before(function () {
    cy.fixture("user.json").then((user) => {
      cy.request({
        method: "POST",
        url: "http://localhost:5000/users/create",
        form: true,
        body: user,
      }).then((response) => {
        userId = response.body._id.$oid;
        email = user.email;
        name = user.firstName + " " + user.lastName;

        // Skapa task
        const newTask = {
          title: "First task",
          description: "Test task",
          userid: userId,
          url: "https://www.youtube.com/watch?v=hLQl3WQQoQ0&list=RDhLQl3WQQoQ0&start_radio=1",
          todos: "First inactive todo item",
        };

        cy.request({
          method: "POST",
          url: "http://localhost:5000/tasks/create",
          form: true,
          body: newTask,
        }).then((response) => {
          taskId = response.body[0]._id.$oid;

          // Skapa active todo
          const activTodo = {
            taskid: taskId,
            description: "active todo item",
            done: "true",
          };

          cy.request({
            method: "POST",
            url: "http://localhost:5000/todos/create",
            form: true,
            body: activTodo,
          });
        });
      });
    });
  });

  beforeEach(function () {
    cy.visit("http://localhost:3001");
    cy.contains("div", "Email Address").find("input[type=text]").type(email);
    cy.get("form").submit();

    cy.get("h1").should("contain.text", "Your tasks, " + name);
    cy.get(".container-element").find("img").click();
    cy.get(".todo-list").should("exist");
  });

  it("should successfully add a new todo item when description field contains text", () => {
    const todoItemText = "New test todo item";

    cy.get('.inline-form input[type="text"]').type(todoItemText, {
      force: true,
    });

    cy.get('.inline-form input[type="submit"]').click({ force: true });

    cy.get(".todo-list li").should("have.length", 3);
    cy.contains(".todo-list li", todoItemText).should("exist");
  });

  it("should disable the add button when description field is empty", () => {
    cy.get('.inline-form input[type="submit"]').should("be.disabled");
  });

  it("should mark todo item as completed with line-through when checker is clicked", () => {
    cy.get(".todo-item")
      .contains("First inactive todo item")
      .parents(".todo-item")
      .within(() => {
        cy.get(".checker").click().should("have.class", "checked");
        cy.get(".editable").should(
          "have.css",
          "text-decoration-line",
          "line-through"
        );
      });
  });

  it("should mark todo item as active without line-through when checker is clicked", () => {
    cy.get(".todo-item")
      .contains("active todo item")
      .parents(".todo-item")
      .within(() => {
        cy.get(".checker").click().should("have.class", "unchecked");
        cy.get(".editable").should(
          "not.have.css",
          "text-decoration-line",
          "line-through"
        );
      });
  });

  it("should successfully delete a todo item when remove button is clicked", () => {
    cy.intercept("DELETE", "/todos/byid/*").as("deleteTodoItem");

    cy.contains(".todo-item", "active todo item").as("item").should("exist");

    cy.get("@item").find("span.remover").click({ force: true });

    cy.wait("@deleteTodoItem");

    cy.contains(".todo-item", "Task to active again", { timeout: 7000 }).should(
      "not.exist"
    );
  });

  after(function () {
    cy.request({
      method: "DELETE",
      url: `http://localhost:5000/tasks/byid/${taskId}`,
    });

    cy.request({
      method: "DELETE",
      url: `http://localhost:5000/users/${userId}`,
    });
  });
});