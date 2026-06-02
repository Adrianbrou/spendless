import { useState } from "react";

// This component owns EVERYTHING about creating a user:
// its own input state, its own send-to-backend function, and its own form.
// App doesn't need to know any of these details - it just renders <CreateUser />.
function CreateUser() {
  // --- LOGIC ZONE (plain JavaScript, draws nothing) ---

  // One state box per input field. They start empty ("").
  const [email, setEmail] = useState("");
  const [name, setName] = useState("");

  // This function runs ONLY when the button is clicked (see onClick below).
  // It sends the typed-in email + name to the backend as JSON.
  function handleCreateUser() {
    fetch("http://127.0.0.1:8000/users/", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ email, name }),
    })
      .then((res) => res.json())
      .then((newUser) => console.log("created:", newUser));
  }

  // --- SCREEN ZONE (the visual form) ---
  return (
    <div>
      <h2>Create User</h2>

      {/* Each input is "wired" to its state box:
          - value={...}     shows what's in the box
          - onChange={...}  puts each keystroke into the box */}
      <input
        value={email}
        onChange={(e) => setEmail(e.target.value)}
        placeholder="email"
      />
      <input
        value={name}
        onChange={(e) => setName(e.target.value)}
        placeholder="name"
      />

      {/* onClick runs handleCreateUser when the button is pressed */}
      <button onClick={handleCreateUser}>Create</button>
    </div>
  );
}

export default CreateUser;
