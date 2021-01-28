

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
        add_post1(data.h[i], data.c[i]);
      }
    })
};

function add_post1(h, c) {
  // Create new post
  const post = document.createElement('div');
  post.className = 'card-body';
  post.append(c);

  const header = document.createElement('h6');
  header.className = "card-header";
  header.append(h);
  post.insertBefore(header, post.childNodes[0])

  // Add post to DOM
  document.querySelector('#posts').append(post);
}