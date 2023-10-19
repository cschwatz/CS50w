document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  // handle email interaction -- the 'click' function passes an 'event' object that contains information 
  // about the target element that was clicked
  // we select the #emails-view because it is a parent element that contails ALL mailDivs
  // by querying the parent, we can use the 'target' function, to see what has been clicked
  document.querySelector('#emails-view').addEventListener('click', (event) => {
    if (event.target.classList.contains('mailDiv')) { // if the clicked target is an email
      let id = event.target.getAttribute('id');
      load_email(id);
    }
  });

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
      mailDiv.className = 'mailDiv';
      mailDiv.id = `${element['id']}`;
      // create divs for the content
      let mailSender = document.createElement('div');
      let mailSubject = document.createElement('div');
      let mailTime = document.createElement('div');
      let archiveButton = document.createElement('button');
      // give ids
      mailSender.id = 'mailSender';
      mailSubject.id = 'mailSubject';
      mailTime.id = 'mailTime';
      archiveButton.className = 'archiveButton';
      archiveButton.id = `${element['id']}`;
      // populate div with necessary content
      mailSender.innerHTML = element['sender'];
      mailSubject.innerHTML = element['subject'];
      mailTime.innerHTML = element['timestamp'];
      // handle archive button
      archiveButton.textContent = 'Archive';
      //append to the email div
      mailDiv.appendChild(mailSender);
      mailDiv.appendChild(mailSubject);
      mailDiv.appendChild(mailTime); 
      mailDiv.appendChild(archiveButton);
      //append email to the div that handles all emails
      allMails.appendChild(mailDiv);
    });
    //append all emails to div that shows the emails in the HTML
    document.querySelector('#emails-view').append(allMails);
  });
  // handle archive button click -- checks if person clicked inside the div that contains the emails
  document.querySelector('#emails-view').addEventListener('click', (event) => {
    if (event.target.classList.contains('archiveButton')) { // if the clicked target is an archive button
      let id = event.target.getAttribute('id'); // get the id of the email whose button was clicked
      fetch(`emails/${id}`, { // update the 'archived' boolean variable to true
        method: 'PUT',
        body: JSON.stringify ({
          archived: true
        })
      })
    }
    load_mailbox('inbox');
  });
}

function load_email(id) {
  // hides other views and only show the current email
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'block';

  // Clear the existing content of the email-view -- if an email was opened before
  document.querySelector('#email-view').innerHTML = '';

  // get the emails id so that we can fetch only a single email
  fetch(`emails/${id}`)
  .then(response => response.json())
  .then(data => {
    let responseData = data;
    // create div that contains ALL content
    let emailDiv = document.createElement('div');
    emailDiv.id = 'emailDiv';
    // create divs for separate content
    let senderDiv = document.createElement('div');
    let recipientsDiv = document.createElement('div');
    let subjectDiv = document.createElement('div');
    let timeDiv = document.createElement('div');
    let bodyDiv = document.createElement('div');
    // give ids 
    senderDiv.id = 'senderDiv';
    recipientsDiv.id = 'recipientsDiv';
    subjectDiv.id = 'subjectDiv';
    timeDiv.id = 'timeDiv';
    bodyDiv.id = 'bodyDiv';
    // populate div with data from JSON fetched from API
    senderDiv.innerHTML = data['sender'];
    recipientsDiv.innerHTML = data['recipients'];
    subjectDiv.innerHTML = data['subject'];
    timeDiv.innerHTML = data['timestamp'];
    bodyDiv.innerHTML = data['body'];
    //append to the email div
    emailDiv.appendChild(senderDiv);
    emailDiv.appendChild(subjectDiv);
    emailDiv.appendChild(recipientsDiv);
    emailDiv.appendChild(timeDiv);
    emailDiv.appendChild(bodyDiv);
    //append all emails to div that shows the email in the HTML
    document.querySelector('#email-view').append(emailDiv);
  });
}