document.addEventListener('DOMContentLoaded', function() {

    document.getElementById('new-post').onclick = post;

}); 

function post() {

    document.getElementById('post-view').style.display = 'block';

}