document.addEventListener('DOMContentLoaded', () => {

    // start by not displaying the edit post area
    const edit_area = document.querySelectorAll('.edit-post-area');
    const post_text = document.querySelectorAll('.post-text');
    const save_button = document.querySelectorAll('.save-changes');
    
    for (const e of edit_area) {
        e.style.display = 'none';
    }

    // display text area if edit button selected
    // hide post text
    const buttons_list = document.querySelectorAll(".edit-button");

    for (let i = 0; i < buttons_list.length - 1; i++) {
        buttons_list[i].addEventListener('click', () => {
        
            if (edit_area[i].style.display === "none") {

                edit_area[i].style.display = "block";
                post_text[i].style.display = "none";

                // if save changes button is clicked, update post
                const post_id = parseInt(edit_area[i].firstElementChild.name);

                save_button[i].addEventListener('click', edit_post.bind(null, post_id, i));
            } else {

                edit_area[i].style.display = "none";
                post_text[i].style.display = "block";
            }
        });
    };

    const heart_buttons = document.querySelectorAll(".bi.bi-suit-heart-fill");

    for (let i = 0; i < buttons_list.length - 1; i++) {

        heart_buttons[i].addEventListener('click', () => {

            const post_id = parseInt(edit_area[i].firstElementChild.name);
            let heart_color = heart_buttons[i].style.color;
            let n_likes = parseInt(document.querySelectorAll('.likes-section')[i].innerHTML);
            
            if (heart_color === '') {
                heart_buttons[i].style.color = 'red';
                document.querySelectorAll('.likes-section')[0].innerHTML = n_likes + 1;
            } else {
                heart_buttons[i].style.color = '';
                document.querySelectorAll('.likes-section')[0].innerHTML = n_likes - 1;
            }

            // increase num_likes in DB
            fetch(`like_post/${post_id}`, {
                method: 'PUT'
            });

        })
    }

})

function edit_post(post_id, div_n) {

    const newText = document.querySelector(`#post-edit-${post_id}`).value;
    
    // edit post
    fetch(`/edit_post/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            text: newText
        })
    })
    .then((res) => {
        console.log(res);

        document.querySelectorAll('.post-text')[div_n].innerHTML = newText;

        // close edit div and show new post
        document.querySelectorAll('.edit-post-area')[div_n].style.display = "none";
        document.querySelectorAll('.post-text')[div_n].style.display = "block";
    });

}