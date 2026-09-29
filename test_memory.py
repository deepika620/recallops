from memory import setup_memory, remember, recall

print("Creating RecallOps memory bank...")

setup_memory()

print("Storing first incident...")

remember("""
Incident ID: INC-1001

Service: Payment API

Severity: SEV-1

Symptoms:
The Payment API started returning HTTP 500 errors.
Error rate increased to 35%.

Recent deployment:
payment-service version 2.8.1

Investigation:
The team discovered that database connections were not
being released correctly.

Attempted fix:
The team increased the database connection pool from 50 to 100.

Result:
FAILED. The error rate remained high.

Successful fix:
The team rolled back payment-service from version 2.8.1
to version 2.8.0.

Outcome:
The error rate returned to normal within four minutes.

Lesson:
Increasing the connection pool did not solve this incident.
Rolling back version 2.8.1 successfully resolved the problem.
""")

print("Incident stored!")

print("\nSearching Hindsight memory...\n")

result = recall(
    "Have we seen a Payment API incident involving "
    "database connection problems, and what solution worked?"
)

for memory in result.results:
    print("MEMORY:")
    print(memory.text)
    print("-" * 60)