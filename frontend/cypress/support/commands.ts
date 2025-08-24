/// <reference types="cypress" />
// ***********************************************
// This example commands.ts shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************

Cypress.Commands.add('fakeLogin', () => {
  cy.intercept('GET', '/v1/auth/status/', { fixture: 'v1/auth/status/get-authenticated.json' }).as('v1-auth-status')

  cy.visit('http://localhost:4173/#/overview', {
    onBeforeLoad (window) {
      window.localStorage.setItem('login', 'true')
    },
  })
})
