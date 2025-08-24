declare namespace Cypress {
  // eslint-disable-next-line @typescript-eslint/no-unused-vars,@typescript-eslint/no-explicit-any
  interface Chainable<Subject = any> {
    fakeLogin(): Chainable<void>
  }
}
