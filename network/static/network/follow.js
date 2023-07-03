document.addEventListener('DOMContentLoaded', function() {
    const follow_form = document.getElementById('follow_form');
    
    if (follow_form) {

        const is_following = document.querySelector('#hidden_is_following').value;
        const follow_button = document.getElementById('follow_button');

        if (is_following == "True"){
            follow_button.className = "btn btn-danger";
            follow_button.value = "Unfollow";
            follow_button.type = "submit";
        }
        else {
            follow_button.className = "btn btn-success";
            follow_button.value = "Follow";
            follow_button.type = "submit";
        } 
        const username = document.querySelector('#hidden-user-general').value;
        document.querySelector('#follow_form').addEventListener('submit', () => follow_or_unfollow(username, follow_button));
    }
});

function follow_or_unfollow(username, follow_button){

    event.preventDefault();

    var followers_number = document.querySelector('#followers-count');

    fetch(`/follow/${username}`, {
        method: 'POST'
      })
      .then(response => response.json())
      .then(data => {
        const action = data.action;

        if (action == "follow") {
            follow_button.className = "btn btn-danger";
            follow_button.value = "Unfollow";
            follow_button.type = "submit";

        }
        else {
            follow_button.className = "btn btn-success";
            follow_button.value = "Follow";
            follow_button.type = "submit";     
        }

        fetch(`/followers-number/${username}`, {
            method: 'POST'
          })
          .then(response => response.json())
          .then(data => {
            followers_number.innerHTML = data.followers;
        })
      })


}