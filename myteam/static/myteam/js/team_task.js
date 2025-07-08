function openTaskPopup(taskid){

    fetch(`/myteam/team-task/${taskid}/`)
    .then (response => response.text())
    .then (html =>{
        document.getElementById("team-task-contianer").innerHTML = html;
        document.getElementById("team-task-modal").style.display = "block";
    });
}

function closePopup(){

    document.getElementById("team-task-modal").style.display = "none";
}