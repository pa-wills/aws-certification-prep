# Simple SQS Producer Consumer
This is a project to demonstrate (I hope) that I know how to use SQS. It's a really simple use case.

* Producer fires every x seconds, generates number between 1..100, pushes message with said number to queue.
* Consumer polls said queue, retreieves message, gets number, adds another number between 1..100 to it, writes output to a DyDB table, deletes message from said queue.
* And I may mess with this a little to experiment with the edge cases.
* I'll define it into a Stack that I can deploy with the sam command line tools. Defining a CI/CD pipeline feels like overkill.
