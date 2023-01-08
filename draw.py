import turtle


def drawChessTable(queens, n):
    sc = turtle.Screen()
    pen = turtle.Turtle()

    sc.setup(800, 800)

    startX = -300
    startY = -200

    pen.speed("fastest")

    dimension = 600 / n

    pen.color("black")

    counter = 0
    for i in range(n):
        queen = queens[n - i - 1]
        for j in range(n):
            pen.up()
            pen.setposition(startX, startY)
            pen.down()

            if j == queen:
                pen.color("red")
            else:
                pen.color("black")

            if (counter % 2 == 0 and i % 2 == 0) or (counter % 2 == 1 and i % 2 == 1) or j == queen:
                pen.begin_fill()

            for k in range(4):
                pen.forward(dimension)
                pen.right(90)

            if (counter % 2 == 0 and i % 2 == 0) or (counter % 2 == 1 and i % 2 == 1) or j == queen:
                pen.end_fill()

            startX += dimension
            counter += 1

        startX = -300
        startY += dimension

    turtle.getscreen()._root.mainloop()
