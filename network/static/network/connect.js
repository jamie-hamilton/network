document.addEventListener('DOMContentLoaded', function() {
    get_follows();
});

let profile_user = parseInt(document.getElementById('profile_user').value);

function get_follows() {
    fetch(`/connect/${profile_user}`)
    .then(response => response.json())
    .then(context => {
        if (profile_user != context.user[0].id) {
            let follow_btn = document.getElementById('follow')
            follow_btn.value = "Follow"
            context.followers.forEach (follower => {
                if (context.user[0].id === follower.id) follow_btn.value = "Unfollow";
            })
        }
        document.getElementById('followers').textContent = context.followers.length;
        document.getElementById('following').textContent = context.following.length;
    })
}

function follow(e) {
    let csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    let connection = e.target['call'].value

    fetch(`/connect/${profile_user}`, {
        credentials: 'include',
        method: 'PUT',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            call: connection,
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        get_follows();
    });
}

document.getElementById('connect').onsubmit = (e) => {
    e.preventDefault();
    follow(e)
}



