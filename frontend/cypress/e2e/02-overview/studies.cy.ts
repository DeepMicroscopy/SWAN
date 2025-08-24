const $ = {
  list: {
    items: 'main .v-list > .v-list-item',
    title: '.v-list-item__content > .v-list-item-title',
    subtitle: '.v-list-item__content > .v-list-item-subtitle',
    href: '.v-list-item__prepend > a.v-btn',
    icon: '.v-list-item__prepend .v-icon',
    action: '.v-list-item__append > .v-btn',
  },
  dialog: {
    container: 'body > .v-overlay-container > .v-dialog',
    title: '.v-dialog .v-card .v-card-title',
    content: '.v-dialog .v-card .v-card-text > div',
    close: '.v-dialog .v-card .v-card-actions > .v-btn',
  },
}

describe('Overview of Studies', () => {
  beforeEach(() => {
    cy.intercept('GET', '/v1/studies/', { fixture: 'v1/studies/list-all.json' }).as('v1-list-studies')

    cy.fakeLogin()
  })

  it('displays multiple studies', () => {
    cy.get($.list.items).should('have.length', 2)
  })

  it('links to study details', () => {
    cy.get($.list.items).each($el => {
      cy.wrap($el).find($.list.href)
        .should('be.visible')
        .invoke('attr', 'href').should('match', /\/studies\/[0-9a-f-]+/)
    })
  })

  it('shows study titles', () => {
    cy.get($.list.items).each($el => {
      cy.wrap($el).find($.list.title)
        .should('be.visible')
        .invoke('text').should('match', /[A-Za-z0-9]/)
    })
  })

  it('shows start and end dates', () => {
    cy.get($.list.items).each($el => {
      cy.wrap($el).find($.list.subtitle)
        .should('be.visible')
        .invoke('text').should('match', /.* - .*/)
    })
  })

  it('opens and closes the description', () => {
    cy.get($.dialog.container).should('not.exist')

    cy.get($.list.items).first().find($.list.action).click()

    cy.get($.dialog.container).should('exist')

    cy.get($.dialog.close).click()

    cy.get($.dialog.container).should('not.exist')
  })

  it('displays the same title in the description', () => {
    cy.get($.list.items).first().find($.list.action).click()

    cy.get($.dialog.title).should('be.visible')

    cy.get($.dialog.title).invoke('text').then(title => {
      cy.get($.list.items).first().find($.list.title).invoke('text').should('match', new RegExp(title.trim()))
    })
  })

  it('displays a markdown description', () => {
    cy.get($.list.items).first().find($.list.action).click()

    cy.get($.dialog.content).should('be.visible')
      .invoke('html').should('match', /<[a-z]+>/)
  })

  it('shows different icons for educational studies', () => {
    const icons: string[] = []

    cy.get($.list.items).each($el => {
      cy.wrap($el).find($.list.icon)
        .should('be.visible')
        .invoke('attr', 'class')
        .then(classes => {
          const mdi = classes!.split(' ').filter(c => c.startsWith('mdi-'))

          expect(mdi).to.have.length.greaterThan(0)
          expect(mdi[0]).length.greaterThan(0)

          icons.push(mdi[0]!)
        })
    })

    cy.then(() => {
      expect(icons).to.have.length.greaterThan(1)
    });
  })
})
