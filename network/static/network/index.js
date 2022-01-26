document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('new-post').onclick = post;

});

function post() {

    document.getElementById('post-view').style.display = 'block';

}

function edit(id) {

    edit_text = document.getElementById(`edit-text-${id}`);
    edit_button = document.getElementById(`edit-button-${id}`);
    edit_text.style.display = 'block';
    edit_button.style.display = 'block';

    edit_button.addEventListener('click', () => {
        fetch(`/edit/${id}`, {
            method: 'PUT',
            body: JSON.stringify({
                content: edit_text.value
            })
        });
        edit_text.style.display = 'none';
        edit_button.style.display = "none";

        document.getElementById(`post-content-${id}`).innerHTML = edit_text.value;
    });
 
}

function like(id) {

    like_button = document.getElementById(`like-button-${id}`);
    
    if (like_button.style.backgroundColor == 'white') {
        fetch(`/like/${id}`, {
            method:'PUT',
            body: JSON.stringify({
                like: true
            })
        });
        like_button.style.backgroundColor = 'red';
    }
    else {
        fetch(`/like/${id}`, {
            method:'PUT',
            body: JSON.stringify({
                like: false
            })
        });

        like_button.style.backgroundColor = 'white';
    }
}