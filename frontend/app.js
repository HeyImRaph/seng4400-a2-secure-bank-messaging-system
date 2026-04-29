const API = "https://fvrilaxyzj.execute-api.us-east-1.amazonaws.com";

function isEmpty(value) {
    return value.trim() === "";
}

function showError(message) {
    alert(message);
}

function selectThread(id) {
    document.getElementById("replyThreadId").value = id;
    document.getElementById("selectedMessageText").innerText =
        "Replying to selected message: " + id;
}

function displayMessages(messages) {
    const messagesDiv = document.getElementById("messages");
    messagesDiv.innerHTML = "";

    if (!messages || messages.length === 0) {
        messagesDiv.innerHTML = "<p>No messages found.</p>";
        return;
    }

    messages.forEach(function (msg) {
        const card = document.createElement("div");
        card.className = "message-card";

        card.innerHTML = `
            <div class="message-header">
                <div>
                    <strong>${msg.subject}</strong>
                    <div class="meta">
                        ${msg.senderName} (${msg.senderRole})
                    </div>
                </div>
            </div>

            <div class="message-body">
               <b>Message:</b> ${msg.messageBody}
            </div>

            <div class="message-footer">
                <small><b><i>click on box to reply</i></b></small>
            </div>
        `;

        card.onclick = function () {
            document.getElementById("replyThreadId").value = msg.threadId;
            document.getElementById("selectedMessageText").innerText =
                "Replying to: " + msg.subject + ", " + msg.senderName;
        };

        messagesDiv.appendChild(card);
    });
}

async function sendMessage() {
    const customerId = document.getElementById("customerID").value;
    const senderName = document.getElementById("name").value;
    const subject = document.getElementById("subject").value;
    const messageBody = document.getElementById("message").value;

    if (isEmpty(customerId) || isEmpty(senderName) || isEmpty(subject) || isEmpty(messageBody)) {
        showError("Please fill in all message fields");
        return;
    }

    const response = await fetch(`${API}/messages`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            customerId: document.getElementById("customerID").value,
            senderName: document.getElementById("name").value,
            subject: document.getElementById("subject").value,
            messageBody: document.getElementById("message").value,
        })
    });

    const data = await response.json();
    alert("Message sent!");
    console.log(data);

    document.getElementById("viewCustomerID").value =
        document.getElementById("customerID").value;

    await getMessages();
}

async function getMessages() {
    const customerID = document.getElementById("viewCustomerID").value;

    let url = "https://fvrilaxyzj.execute-api.us-east-1.amazonaws.com/messages";

    if (customerID && customerID.trim() !== "") {
        url += "/" + customerID;
    }

    const response = await fetch(url);
    const data = await response.json();

    displayMessages(data.messages);
}

async function replyMessage() {
    const threadId = document.getElementById("replyThreadId").value;
    const staffName = document.getElementById("staffName").value;
    const messageBody = document.getElementById("replyMessage").value;

    if (isEmpty(threadId) || isEmpty(staffName) || isEmpty(messageBody)) {
        showError("Please fill in all staff reply fields.");
        return;
    }

    const response = await fetch(`${API}/messages/${threadId}/reply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
            staffName: document.getElementById("staffName").value,
            messageBody: document.getElementById("replyMessage").value
        })
    });

    const data = await response.json();
    alert("Reply sent!");
    console.log(data);

    await getMessages();
}