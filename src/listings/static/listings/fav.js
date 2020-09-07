    /* const conatin api url */
    const DEV = false
    const API_URL = DEV ? 'http://localhost:8000/api/toggle_fav' : 'https://samehabouelsaad.pythonanywhere.com/api/toggle_fav';


    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }


    /* async function to send data to our server with delete method */
    async function toggleFav(path, data) {

        const response = await fetch(path, {
            method: 'POST',
            mode: 'same-origin',  // Do not send CSRF token to another domain.

            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(data)
        });
        return await response.json();
    }


    /* async function to update user interface with a message from the server */
    async function updateUI(data) {
        if (data['liked']) {
            document.querySelector(`[data-id="${data.id}"]`).classList.add("btn-warning");
        } else {
            document.querySelector(`[data-id="${data.id}"]`).classList.remove("btn-warning");
        }
    }




    /* main function to run when page loaded */
    function main() {
        /* get all html elements with class 'toggle-button */
        const toggleButton = document.querySelectorAll('.toggle-button');

        /* Attach event listenr to each button to invoke when user click it */
        toggleButton.forEach((button) => {
            button.addEventListener('click', toggleHnad, false);
        });

        /* function to run when user click a delete button */
        function toggleHnad(ev) {
            console.log(this.dataset.id)

            /* create object contain the data we need to send it to server api */
            const serverData = {
                id: this.dataset.id,
            }

            /* call this functio with api url and data to invoke async fetch and set a callback function to run when server respond */
            toggleFav(API_URL, serverData).then((data) => {
                updateUI(data);
            });
        }
    }

    document.addEventListener('DOMContentLoaded', main);
