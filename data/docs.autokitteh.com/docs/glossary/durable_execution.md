---
sidebar_position: 1
---

# Durable Execution

Durable execution is a concept often related to computing and software systems, particularly in the context of distributed systems, workflows, and long-running processes. It refers to the ability of a system to maintain and continue execution processes reliably over long periods, even in the face of failures, errors, or interruptions. This includes resilience to hardware failures, network issues, software crashes, and other unforeseen disruptions.

Key aspects of durable execution include:

- **Fault Tolerance:** The system can recover from and continue execution after a failure occurs, whether it's a hardware malfunction, software bug, or other issues.
- **State Persistence:** The system maintains its state across crashes or restarts. This often involves saving the execution state to a durable storage system (like a database) so that it can be restored and execution can resume from a known point.
- **Scalability:** The ability to handle increased load by adding resources without affecting the ongoing processes or their durability.
- **Consistency:** Ensuring that the system's state remains consistent, even in the face of failures, which is crucial for systems that manage transactions or maintain critical data.
- **Reliability:** The overall system design ensures that the execution can reliably proceed to completion, even if it takes a long time or encounters various challenges.

AutoKitteh is powered by [Temporal](https://www.temporal.io) providing a durable execution engine.

## Example: The Need for Durable Execution

Consider a money transfer between two accounts. In this process, the system needs to ensure that money deducted from one account is reliably credited to another, even if there are system failures during the transaction. The key steps in a money transfer might include:

- Create transaction id
- Withdraw from Sender's Account
- Deposit tothe Receiver's Account

In a durable execution context, this process must be atomic—either both steps are completed successfully, or neither is, ensuring that money isn't lost or created out of thin air. This is often achieved using a transaction mechanism that can roll back changes if any part of the process fails.

A simplified code may look something like, as long as the functions are atomic and idempotent:

```
def transfer(withdraw_account, deposit_account, amount):
    transaction_id = get_transaction_id()
    withdraw_from_account_route(transaction_id, withdraw_account, amount)
    deposit_to_account_route(transaction_id, deposit_account, amount)
```

Check out the [demos](../use_cases).

## The Magic 🪄 of Durable Execution for Developers

Writing long-running workflows is very hard in distributed systems composed of services. The key challenges are: synchronizing asynchronous events, managing a complex state machine, and handling errors, including malfunctions in internal infrastructure as well as external services.

Consider the flow above, in real life, the function `withdraw_from_account_route()` may take time. Keeping a process running and waiting asynchronously for workflow events is not efficient. Thus developers typically build a stateful flows where each received event needs to construct the context in the state machine, execute an action, and save the new state. This process is hard to develop and debug, and is prone to bugs.

Developing workflows using duarble execution, as can see in the example above, can save tons of time and make the code robust and easy to develop and manage.
