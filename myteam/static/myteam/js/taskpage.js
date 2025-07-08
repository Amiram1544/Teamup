function showTab(tabName) {

    //First hide all
    document.getElementById("todo").style.display = "none";
    document.getElementById("task").style.display = "none";
    document.getElementById("unknown").style.display = "none";

    //Remove active
    document.querySelectorAll(".tab-link").forEach(link => link.classList.remove("active"))

    //Selected tab show
    document.getElementById(tabName).style.display = "block"

    //if active
    if (tabName == 'todo') {
        document.getElementById('tab-todo').classList.add("active")
    } else if (tabName== 'task') {
        document.getElementById('tab-task').classList.add("active")
        loadTeamTask()
    } else if (tabName== 'unknown') {
        document.getElementById('tab-unknown').classList.add("active")
    }
}

function loadTeamTask() {
    fetch(`/myteam/get-user-tasks/`)
    .then (response => response.text())
    .then (html => {
        document.getElementById("team-task-container").innerHTML = html;
    })
}

function openTaskModal() {
    
    const topic = document.getElementById("task-topic").value.trim();

    if (!topic) {
        alert("You must Enter a topic first.");
        return;
    }

    document.getElementById("task-modal").style.display = "flex";

}

function closeTaskModal(){

    document.getElementById("task-modal").style.display = "none";

    document.getElementById("task-notes").value = '';
    document.getElementById("task-description").value = '';
}

function submitTask() {

    const topic = document.getElementById("task-topic").value.trim();
    const description = document.getElementById("task-description").value.trim();
    const notes = document.getElementById("task-notes").value.trim();

    if (!topic) {
        alert("You must Enter a topic first.");
        return;
    }

    fetch("/myteam/add-task-ajax/", {
        method : "POST",
        headers : {
            "Content-Type" : "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({
            topic: topic,
            description: description,
            notes:  notes
        })
    })
    .then(response => response.json())
    .then(data =>{
        if (data.success) {
            addTaskToPage(data.task);
            closeTaskModal();

            document.getElementById("task-topic").value = '';

        } else {
            alert("Failed");
        }
    });

    
}

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


function addTaskToPage(task) {
    
    const container = document.querySelector(".to-do");

    const taskElement = document.createElement("div");
    taskElement.classList.add("todo-items");
    taskElement.dataset.id = task.id;

    taskElement.innerHTML = `
        <ul>
            <li><span class="task-topic">${ task.topic }</span>
            <button type="button" onclick="doneButton(this)" class="button done-button">✅</button>
            <button type="button" onclick="deleteButton(this)" class="button delete-button">🗑️</button></li>
            <span class="task-description">${ task.description }</span>
            <span class="task-notes">${ task.notes }</span>
        </ul>
    `;

    if (task.completed) {

        taskElement.classList.add('completed');
    }

    container.insertBefore(taskElement, container.firstChild);
}

 
function doneButton(button) {

    const taskElement = button.closest(".todo-items");
    const taskId = taskElement.dataset.id;
    console.log("Toggling completed for task id:", taskElement.dataset.id);
    taskElement.classList.toggle("completed"); // toggle CSS class for visual

    fetch("/myteam/complete-task-ajax/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ id: taskId })
    })
    .then(response => response.json())
    .then(data => {
        if (!data.success) {
            alert("Failed to update task status.");
            // revert toggle?
            taskElement.classList.toggle("completed");
        }
    });
}

function deleteButton(button){

    const taskElement = button.closest(".todo-items")
    console.log("Deleting task element:", taskElement);
    const taskId =taskElement.dataset.id;

    fetch("/myteam/delete-task-ajax/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": getCookie("csrftoken")
        },
        body: JSON.stringify({ id: taskId })
    })
    .then (response => response.json())
    .then (data =>{
        if (data.success){
            taskElement.remove();
        } else {
            alert("Failed to delete")
        }
    });
}