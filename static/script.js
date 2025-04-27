$(document).ready(function() {
    $('#sendBtn').click(function() {
        var userMessage = $('#userMessage').val();
        if (userMessage.trim() === "") return; // Prevent sending empty messages

        // Append user message to chat
        $('#chatBox').append(`<div class="user-message">${userMessage}</div>`);
        $('#userMessage').val(""); // Clear input field

        // Send message to Flask backend (your API)
        $.ajax({
            type: 'POST',
            url: '/chat',
            contentType: 'application/json',
            data: JSON.stringify({ message: userMessage }),
            success: function(response) {
                var botReply = response.reply;
                $('#chatBox').append(`
                    <div class="bot-message">
                        <img src="https://www.oshukai.fr/wp-content/uploads/2024/11/portrait-Sensei-recadre-247x300.jpg" alt="Bot Profile">
                        ${botReply}
                    </div>
                `);
                $('#chatBox').scrollTop($('#chatBox')[0].scrollHeight); // Scroll to bottom
            },
            error: function() {
                $('#chatBox').append('<div class="bot-message">Error: Could not get response.</div>');
            }
        });
    });

    // Allow pressing 'Enter' to send the message
    $('#userMessage').keypress(function(e) {
        if (e.which == 13) {
            $('#sendBtn').click();
        }
    });
});