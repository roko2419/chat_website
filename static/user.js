$(function() {
          $('#join_chat').bind('click', function() {
            document.getElementById("disappear").innerHTML = '<h3 STYLE="color: greenyellow">CONNECTED</h3>'
            $.getJSON('/join_chat',
                function(data) {

            });
            return false;
          });
});

$(function() {
          $('#send').bind('click', function() {
            var value = document.getElementById("send_msg").value
              console.log(value)
              document.getElementById("send_msg").value = ""

            $.getJSON('/send',
                {val:value},
                function(data) {

            });

            return false;
          });
});

document.getElementById("join_chat").onclick = function (){
    console.log("just ones")
    document.getElementById("exit_button").innerHTML = '<button type="submit" name="exit" formmethod="post" class="btn btn-danger">Exit Chat</button>'
    var update_loop = setInterval(update, 100);
    update()

};

function update(){
    fetch('/get_messages')
        .then(function (response) {
            return response.json();
        }).then(function (text) {
            var messages = "";
            for( value of text["messages"]){
                console.log(text)
                messages = messages + "<br>" + value;
            }
            document.getElementById("display").innerHTML = messages;
    });
    console.log("working");
};

