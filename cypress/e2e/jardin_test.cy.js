

describe('logeo', () => {
  it('MalLogeo', () => {
    cy.visit('https://jardinhorten.onrender.com/accounts/login');
    cy.get('input[type="text"][name="username"]').type('usuario');
    cy.get('input[type="password"][name="password"]').type('hortensia');
    cy.get('button[type="submit"]').click();
  })
  it('BuenLogeo', () => {
    cy.visit('https://jardinhorten.onrender.com/accounts/login');
    cy.get('input[type="text"][name="username"]').type('user');
    cy.get('input[type="password"][name="password"]').type('usuario2023');
    cy.get('button[type="submit"]').click();
  })
});
describe('Comentario', () => {
  it('MalComentario', () => {
    cy.visit('https://jardinhorten.onrender.com/accounts/login/?next=/valorar/');
    cy.get('input[type="text"][name="username"]').type('user');
    cy.get('input[type="password"][name="password"]').type('usuario2023');
    cy.get('button[type="submit"]').click();
    cy.get('#5estrella').click();
    cy.get('#comentar').type('¨*}{+');
    cy.get('button[class="submit"]').click();
  })
  it('BuenComentario', () => {
    cy.visit('https://jardinhorten.onrender.com/accounts/login/?next=/valorar/');
    cy.get('input[type="text"][name="username"]').type('user');
    cy.get('input[type="password"][name="password"]').type('usuario2023');
    cy.get('button[type="submit"]').click();
    cy.get('#5estrella').click();
    cy.get('#comentar').type('Buen lugar');
    cy.get('button[class="submit"]').click();
  })
});
