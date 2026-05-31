import ExpenseItem from "./components/ExpenseItem";

function App() {

  let expenses = [
    { id: 1001, description: "Netflix", amount_cents: 299 },
    { id: 1002, description: "Coffee", amount_cents: 500 },
    { id: 1003, description: "Gas", amount_cents: 4500 },
  ];

  return (
    <div>
      <h1>Spendless</h1>
      <p>Hello from React</p>

      <h2>Expenses</h2>
      <ul>
        {expenses.map((expense) => (
          <ExpenseItem key={expense.id} expense={expense} />
        ))}
      </ul>
    </div>
  );
}

export default App;
