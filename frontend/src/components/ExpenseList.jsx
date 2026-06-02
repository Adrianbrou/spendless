import { useState, useEffect } from "react";
import ExpenseItem from "./ExpenseItem";

// This component owns EVERYTHING about the expense list:
// it fetches the expenses from the backend, holds them in state,
// and draws one ExpenseItem row per expense.
function ExpenseList() {
  // --- LOGIC ZONE ---

  // State box holding the expenses. Starts empty, fills in after the fetch.
  const [expenses, setExpenses] = useState([]);

  // Runs ONCE when this component first appears (that's what the [] means).
  useEffect(() => {
    fetch("http://127.0.0.1:8000/expenses/?user_id=1")
      .then((res) => res.json())
      .then((data) => setExpenses(data));
  }, []);

  // --- SCREEN ZONE ---
  return (
    <div>
      <h2>Expenses</h2>
      <ul>
        {/* One ExpenseItem row per expense in the list */}
        {expenses.map((expense) => (
          <ExpenseItem key={expense.id} expense={expense} />
        ))}
      </ul>
    </div>
  );
}

export default ExpenseList;
