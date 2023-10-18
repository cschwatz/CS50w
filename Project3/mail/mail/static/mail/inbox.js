document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // handle email interaction
  document.querySelector('#mailDiv').addEventListener('click', () => load_email());

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';

  // submit POST request to the mail API to send the mail
  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
      recipients: 'test@test.com',
      subject: 'Meeting time',
      body: 'How about we meet tomorrow at 3pm?'
    })
  })
  .then(response => response.json())
  .then(result => console.log(result));


}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

// submit GET request to the Mail API
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(data => {
    console.log(data);
    let responseData = data; // its an array of results (JSON)
    let allMails = document.createElement('div'); // div that handles all emails in the specific mailbox
    allMails.id = 'allMails';
    responseData.forEach(element => {
      let mailDiv = document.createElement('div'); // div for a single email (box that has border)
      mailDiv.id = 'mailDiv';
      // create divs for the content
      let mailSender = document.createElement('div');
      let mailSubject = document.createElement('div');
      let mailTime = document.createElement('div');
      // give ids
      mailSender.id = 'mailSender';
      mailSubject.id = 'mailSubject';
      mailTime.id = 'mailTime';
      // populate div with necessary content
      mailSender.innerHTML = element['sender'];
      mailSubject.innerHTML = element['subject'];
      mailTime.innerHTML = element['timestamp'];
      //append to the email div
      mailDiv.appendChild(mailSender);
      mailDiv.appendChild(mailSubject);
      mailDiv.appendChild(mailTime); 
      //append email to the div that handles all emails
      allMails.appendChild(mailDiv);
    });
    //append all emails to div that shows the emails in the HTML
    document.querySelector('#emails-view').append(allMails);
  });
  
  function load_email() {
    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-view').style.display = 'block';
    
  }
    

}