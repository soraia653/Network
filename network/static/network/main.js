document.addEventListener('DOMContentLoaded', () => {

    document.querySelector('#allPosts').addEventListener('click', load_all_posts);

    load_all_posts();
});

function load_all_posts() {

    // fetch all posts

    fetch("/all-posts")
    .then(response => response.json())
    .then(posts => {

        for (i in posts) {

            console.log(posts[i]);
            
            const user = posts[i]['user'];
            const text = posts[i]['post'];
            const date = posts[i]['date'];
            const likes = posts[i]['num_likes'];

            // display all posts
            let div = document.createElement('div');
            div.className = 'unique-post';

            div.innerHTML = `
            <div>${user}</div>
            <div>${text}</div>
            <div>${date}</div>
            <div>${likes} likes</div>
            `
            ;

            document.getElementById('all-posts').appendChild(div);


        }
    });
}