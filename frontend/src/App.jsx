import CreateUser from "./components/CreateUser";
import ExpenseList from "./components/ExpenseList";

// App is the page. Its only job now: lay out the page by placing the
// feature components. Each feature handles its own data and logic inside itself.
function App() {
  return (
    <div>
      <h1>Spendless</h1>

      {/* The create-user form (owns its own state + POST) */}
      <CreateUser />

      {/* The expense list (owns its own fetch + state) */}
      <ExpenseList />
    </div>
  );
}

export default App;
