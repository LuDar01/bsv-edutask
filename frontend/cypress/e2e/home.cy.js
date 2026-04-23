describe("Documents flow", () => {
  beforeEach(() => {
    cy.intercept("GET", "/api/document", { fixture: "documents.json" }).as(
      "getDocuments"
    );
    cy.visit("http://localhost:3001");
    cy.wait("@getDocuments");
  });

  it("should show a list of documents", () => {
    cy.get("h2 a").should("have.length", 2);
    cy.contains("Doc 1");
    cy.contains("Doc 2");
  });

  it("should truncate content to 20 characters", () => {
    cy.get(".prose")
      .first()
      .invoke("text")
      .should("match", /^.{20}...$/);
  });

  it("should navigate to a single document page", () => {
    cy.intercept("GET", "/api/document/1", {
      statusCode: 200,
      body: {
        document: { _id: "1", title: "Doc 1", content: "Full content here" },
      },
    }).as("getDocument");

    cy.contains("Doc 1").click();
    cy.wait("@getDocument");
    cy.url().should("include", "/1");
    cy.contains("Full content here");
  });
});
