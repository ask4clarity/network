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