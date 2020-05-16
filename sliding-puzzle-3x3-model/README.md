# Sliding PUzzle Sovler for 3x3
In this project I created a NN to predict the distance to solve given a board state.
This is useful for the solver. The solver works by trying all game routes till it finds
the fastest solve. The issue with this is that there is no thought, just folllow all the
paths. Sometime the solver needs guidance to make it faster and more performant.
I use this model as a *heuristic* to guide the solver to follow that create boards that
are closer to being solved.

## See the live project
[Sliding Puzzle Solver](jshams.github.io/sliding-puzzle/frontend)

## Did the model help?
Yes! With the current vanilla solver in place, about 80K board states were required to be
visited and stored in memory in order to find a solve. With my current *heristic*, manhattan
distance, it took about 600-1000 routes to check, and with this added heuristic, the sover
only needed to search about 60-100 routes.

## Did I dockerize and push to AWS?
No, but I am figuring out ways to publish my model with another resource because I have
been having insane Docker issues.

## Next Steps:
Applying the same concepts with 3x3 board to larger sized boards.
Pushing the API and allowing it to b used by my project.