function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function deleteNotif(feedId, buttonElement) {
    fetch("/myteam/delete-notif/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ feed_id: feedId})
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            const li = buttonElement.closest("li");
            if (li) {
                li.remove();
            }
        } else {
            alert("Failed to delete notification.");
        }
    });
}