document.addEventListener('DOMContentLoaded', function() {

    // show edit form on edit button clicks
    document.querySelectorAll('.btn-edit').forEach (el => {
        el.onclick = (e) => {
            show_edit(e)
        }
    })
    // hide edit button forms on cancel click
    document.querySelectorAll('.btn-cancel').forEach (el => {
        el.onclick = (e) => {
            complete_edit(e)
        }
    })
    // handle edit form submissions
    document.querySelectorAll('.edit-form').forEach (el => {
        el.onsubmit = (e) => {
            e.preventDefault()
            edit(e)
        }
    })
    // handle page likes
    document.querySelectorAll('.like-form').forEach (el => {
        // Update class on post liked by user
        if (el['liked'].value === "") el['liked'].value = "not-hot";
        let post_id = el['post_id'].value;
        let like_el = document.querySelector(`#like-count-${post_id}`)
        let like_count = parseInt(el['count'].value)
        like_el.textContent = like_count
        check_heat(el)
        el.onsubmit = (e) => {
            e.preventDefault()
            // flip like value on submit & update like count
            el['liked'].value === "hot" ? el['liked'].value = 'not-hot' :  el['liked'].value = 'hot'
            
            // add relevant animation class to post
            let animation_class;
            el['liked'].value === "hot" ? animation_class = "heat-up" : animation_class = "cool-down";
            el.querySelector('i').classList.add(animation_class)

            // wait until 'like' animation end to run processes
            setTimeout(function() {
                // update like counter in view
                el['liked'].value === "hot" ? like_count++ : like_count--;
                like_el.textContent = like_count

                // like post
                like(e)
                el.querySelector('i').classList.remove(animation_class)
            }, 500);
        }
    })
});

function show_edit(e) {
    let post = e.target.closest(".post")
    let post_text = post.querySelector('.post-text')
    let edit_form = post.querySelector('.edit-form')

    edit_form["edited"].textContent = post_text.textContent
    edit_form.style.display = 'block';
    post_text.style.display = 'none';
    post.querySelector('.btn-edit').style.display = 'none';
}

function complete_edit(e, data=false) {
    let post = e.target.closest(".post")
    let post_text = post.querySelector('.post-text')
    let edit_form = post.querySelector('.edit-form')
    let edit_btn = post.querySelector('.btn-edit')
    let edited = post.querySelector('.date-edited')

    edit_form.style.display = 'none';
    // if data entered, update was successful so edit post
    if (data) {
        post_text.textContent = data["post"];
        edited.textContent = data["date_edited"];
    }
    post_text.style.display = 'inline-flex';
    edit_btn.style.display = 'block';
}

function edit(e) {
    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    const profile_id = e.target['profile_id'].value
    const post_id = e.target['post_id'].value
    const edited = e.target['edited'].value

    fetch(`/edit/${profile_id}/${post_id}`, {
        credentials: 'include',
        method: 'PUT',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            edited: edited,
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        complete_edit(e, result)
    });
}

function check_heat(el) {
    if (el['liked'].value === "hot") {
        el.querySelector('i').classList.remove('not-hot')
        el.querySelector('i').classList.add('hot')
    }
    else {
        el.querySelector('i').classList.remove('hot')
        el.querySelector('i').classList.add('not-hot')
    }
}

function like(e) {
    const csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
    const user_id = e.target['user_id'].value
    const post_id = e.target['post_id'].value

    fetch(`/like/${post_id}`, {
        credentials: 'include',
        method: 'POST',
        mode: 'same-origin',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        body: JSON.stringify({
            user: user_id,
        })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
        check_heat(e.target)
    });
}