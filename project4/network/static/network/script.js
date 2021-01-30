

// Start with first post
let counter = 1;

// Load posts 20 at a time
const quantity = 5;

// When DOM loads, render the first 20 posts
document.addEventListener('DOMContentLoaded', load);

// If scrolled to bottom, load the next 20 posts
window.onscroll = () => {
    if (window.innerHeight + window.scrollY >= document.body.offsetHeight) {
        load();
    }
};

// Load next set of posts
function load() {
    // Set start and end post numbers, and update counter
    const start = counter;
    const end = start + quantity - 1;
    counter = end + 1;

    // Get new posts and add posts
    fetch(`/fetch_posts?start=${start}&end=${end}`)
    .then(response => response.json())
    .then(data => {
      let n = Object.keys(data.c).length 
      for (var i=0; i<=n; i++) {
        add_post(data.h[i], data.c[i], data.posts[i], data.l[i]);
      }
    })
};

function add_post(h, c, p, l) {
  // Create new post
  const post = document.createElement('div');
  post.className = 'card-body';
  post.append(c);

  const blike = document.createElement('button');
  blike.className = "btn btn-primary";
  let id = "blike" + p
  blike.id = id
  blike.append(l + " likes");
  blike.addEventListener("click",
    function() {
      let post_id = p
      fetch(`/add_like?post_id=${post_id}`)
      .then(response => response.json())
      .then(data => {
        document.querySelector("#" + blike.id).innerHTML = data.n_likes + " likes"
      })

  })

  const header = document.createElement('h6');
  header.className = "card-header";
  header.append(h);
  header.appendChild(blike)
  post.insertBefore(header, post.childNodes[0]);

  // Add post to DOM
  document.querySelector('#posts').append(post);
}