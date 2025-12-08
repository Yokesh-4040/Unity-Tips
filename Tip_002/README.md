# #UNITY TIPS 002/100

# Extending Enums in Unity: Adding Convenience Methods Through Extension Methods

Enums are commonly used in Unity to define sets of related constants—directions, states, types, and more. However, many developers don't realize that you can add behaviour to enums using extension methods, making them more powerful and reducing repetitive logic throughout your codebase.

By extending enums with custom methods, you can encapsulate common operations and transformations directly where they logically belong, leading to cleaner and more maintainable code.

---

## The Problem: Repetitive Logic Around Enums

When working with enums like directional movement on a grid, you often need utility functions to:

* Get the opposite direction
* Convert a direction to a vector
* Rotate directions
* Check if two directions are perpendicular

Without extension methods, this logic either gets scattered across multiple classes or bundled into static utility classes, making the code harder to discover and maintain.

---

## The Solution: Extension Methods for Enums

C# allows you to create extension methods for any type, including enums. This means you can add methods that appear to belong to the enum itself, keeping related logic organized and accessible.

---

## Basic Example: Direction Enum with Extensions

### Define the Enum

```csharp
public enum Direction
{
    Up,
    Down,
    Left,
    Right
}
```

### Create Extension Methods

```csharp
using UnityEngine;

public static class DirectionExtensions
{
    public static Direction Opposite(this Direction direction)
    {
        return direction switch
        {
            Direction.Up => Direction.Down,
            Direction.Down => Direction.Up,
            Direction.Left => Direction.Right,
            Direction.Right => Direction.Left,
            _ => direction
        };
    }

    public static Vector2Int ToVector(this Direction direction)
    {
        return direction switch
        {
            Direction.Up => Vector2Int.up,
            Direction.Down => Vector2Int.down,
            Direction.Left => Vector2Int.left,
            Direction.Right => Vector2Int.right,
            _ => Vector2Int.zero
        };
    }

    public static Direction RotateClockwise(this Direction direction)
    {
        return direction switch
        {
            Direction.Up => Direction.Right,
            Direction.Right => Direction.Down,
            Direction.Down => Direction.Left,
            Direction.Left => Direction.Up,
            _ => direction
        };
    }

    public static Direction RotateCounterClockwise(this Direction direction)
    {
        return direction switch
        {
            Direction.Up => Direction.Left,
            Direction.Left => Direction.Down,
            Direction.Down => Direction.Right,
            Direction.Right => Direction.Up,
            _ => direction
        };
    }

    public static bool IsPerpendicular(this Direction direction, Direction other)
    {
        return direction == Direction.Up && (other == Direction.Left || other == Direction.Right)
            || direction == Direction.Down && (other == Direction.Left || other == Direction.Right)
            || direction == Direction.Left && (other == Direction.Up || other == Direction.Down)
            || direction == Direction.Right && (other == Direction.Up || other == Direction.Down);
    }
}
```

### Usage in Your Game Code

```csharp
public class GridMovement : MonoBehaviour
{
    private Direction currentDirection = Direction.Up;

    void Update()
    {
        if (Input.GetKeyDown(KeyCode.Space))
        {
            // Get the opposite direction
            Direction opposite = currentDirection.Opposite();
            Debug.Log($"Opposite of {currentDirection} is {opposite}");
        }

        if (Input.GetKeyDown(KeyCode.R))
        {
            // Rotate the direction
            currentDirection = currentDirection.RotateClockwise();
            Debug.Log($"Rotated to {currentDirection}");
        }

        if (Input.GetKeyDown(KeyCode.M))
        {
            // Move in the current direction
            Vector2Int moveVector = currentDirection.ToVector();
            transform.position += new Vector3(moveVector.x, moveVector.y, 0);
        }
    }
}
```

---

## Benefits of This Approach

* **Improved Discoverability**: When you type `Direction.Up.`, IntelliSense shows all available extension methods
* **Cleaner Code**: No need for separate utility classes or helper methods
* **Better Organization**: Related functionality lives close to the enum definition
* **Easier Testing**: Extension methods are static and easy to unit test
* **Consistent API**: The enum feels like it has built-in methods

---

## Real-World Unity Use Cases

### 1. Grid-Based Movement
```csharp
Vector2Int nextPosition = currentPosition + playerDirection.ToVector();
```

### 2. AI Pathfinding
```csharp
Direction pathDirection = CalculatePath();
if (pathDirection.IsPerpendicular(currentFacing))
{
    // Need to turn before moving
}
```

### 3. Combat Systems
```csharp
Direction attackDirection = GetAttackInput();
Direction blockDirection = enemyPosition.Opposite();
```

### 4. Puzzle Mechanics
```csharp
Direction rotatedDirection = currentDirection.RotateClockwise();
```

---

## Best Practices

1. **Keep Extensions Focused**: Only add methods that are universally useful for the enum
2. **Avoid State**: Extension methods should be stateless—they work with the enum value passed to them
3. **Use Static Classes**: Always define extension methods in static classes
4. **Namespace Organization**: Consider placing extensions in a dedicated namespace like `YourGame.Extensions`
5. **Document Your Extensions**: Add XML documentation comments to help other developers

---

## Common Patterns

### Color State Extensions
```csharp
public enum TeamColor { Red, Blue, Green, Yellow }

public static class TeamColorExtensions
{
    public static Color ToUnityColor(this TeamColor teamColor)
    {
        return teamColor switch
        {
            TeamColor.Red => Color.red,
            TeamColor.Blue => Color.blue,
            TeamColor.Green => Color.green,
            TeamColor.Yellow => Color.yellow,
            _ => Color.white
        };
    }
}
```

### Game State Extensions
```csharp
public enum GameState { Menu, Playing, Paused, GameOver }

public static class GameStateExtensions
{
    public static bool CanReceiveInput(this GameState state)
    {
        return state == GameState.Playing;
    }

    public static bool ShowsUI(this GameState state)
    {
        return state != GameState.Playing;
    }
}
```

---

## Conclusion

Extension methods transform enums from simple constant containers into more expressive, self-documenting types. This pattern is especially valuable in Unity projects where directional logic, state machines, and type-based behaviour are common.

By centralizing enum-related operations in extension methods, you create code that's easier to read, maintain, and extend as your project grows.

---

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*
