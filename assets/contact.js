document.addEventListener('DOMContentLoaded', function () {
    const contactForm = document.getElementById('contact-form');
  
    if (!contactForm) {
      console.error('Contact form not found!');
      return;
    }
  
    contactForm.addEventListener('submit', async function (e) {
      e.preventDefault();
  
      const formData = new FormData(this);
      const data = {
        name: formData.get('name'),
        email: formData.get('email'),
        message: formData.get('message'),
      };
  
      try {
        const response = await fetch('https://p06onq8ff9.execute-api.eu-west-2.amazonaws.com/submit', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(data),
        });
  
        const result = await response.json();
  
        if (response.ok) {
          alert('Your message has been sent successfully!');
          this.reset(); // Clear the form
        } else {
          alert('Error: ' + (result.error || 'Unknown error occurred.'));
        }
      } catch (err) {
        console.error('Error submitting form:', err);
        alert('There was an error sending your message. Please try again.');
      }
    });
  });
  