//Reply to the message


function ReplyTo(id, user, body) {

    document.getElementById('parent_id').value = id;
    document.getElementById('reply-to').style.display = 'block';
    document.getElementById('replying-user').textContent = `${user}:`;
    document.getElementById('replying-preview').textContent = body.substring(0, 50);

}

//Cancle reply

function CancleReply(){

    document.getElementById('parent_id').value = '';
    document.getElementById('reply-to').style.display = 'none';
}
