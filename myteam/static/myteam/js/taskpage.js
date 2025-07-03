/*function showTab(tabName) {
    const sections = document.querySelectorAll('.tab-section');
    sections.forEach(section => section.style.display = 'none');

    document.getElementById(tabName).style.display = 'block';
}*/

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
    taskElement.innerHTML = `
        <ul>
            <li><span>${ task.topic }</span></li>
            <span class="task-description">${ task.description }</span>
            <span class="task-notes">${ task.notes }</span>
        </ul>
    `;
    container.appendChild(taskElement);
}

//make this right the guide is in AI
//read the explainment of AJAX and ... 
function doneButton(this) {
    
    document.getElementById("mytopic").style.textDecoration = "line-through";
    document.getElementById("mydesc").style.textDecoration = "line-through";
    document.getElementById("mynotes").style.textDecoration = "line-through";
}