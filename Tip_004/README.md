# #UNITY TIPS 004/100

## Calculating the Closest Point on a Ray

Understanding how to find the closest point on a ray to a given point in space is a fundamental skill in 3D game development. This mathematical technique appears in countless scenarios, from AI pathfinding and projectile prediction to snap-to-line mechanics and distance calculations. While Unity provides some built-in tools for certain cases, mastering the underlying vector mathematics gives you the flexibility to solve a wide range of spatial problems efficiently.

The technique uses vector projection, a powerful mathematical operation that allows you to determine how far along a ray a perpendicular line from your target point would intersect. This creates numerous opportunities for elegant solutions to common game development challenges.

## The Problem

When working with rays in 3D space, you often need to find the point on the ray that is closest to another point. Common scenarios include:

- **AI Navigation**: Determining how close an agent is to a patrol path
- **Cable Physics**: Simulating cables that need to snap to guide lines
- **Projectile Tracking**: Finding the closest approach distance of a moving object
- **Weapon Systems**: Calculating lead points for target prediction
- **Editor Tools**: Creating snap-to-line functionality for level design

Without understanding the mathematical approach, developers often resort to iterative sampling along the ray, which is computationally expensive and imprecise.

## The Solution

The solution uses **vector projection** through the dot product. By projecting the vector from the ray's origin to your target point onto the ray's direction, you can calculate exactly how far along the ray the closest point lies.

The formula is straightforward:
```
t = Vector3.Dot(point - rayOrigin, rayDirection)
closestPoint = rayOrigin + rayDirection * t
```

Where `t` represents the distance along the ray (assuming the ray direction is normalized).

## Code Examples

### Basic Implementation

```csharp
public static Vector3 GetClosestPointOnRay(Vector3 rayOrigin, Vector3 rayDirection, Vector3 point)
{
    // Project the vector from ray origin to point onto the ray direction
    float t = Vector3.Dot(point - rayOrigin, rayDirection);

    // Calculate the closest point
    Vector3 closestPoint = rayOrigin + rayDirection * t;

    return closestPoint;
}
```

### Example 1: AI Path Following with Distance Check

```csharp
public class AIPathFollower : MonoBehaviour
{
    [SerializeField] private Transform pathStart;
    [SerializeField] private Transform pathEnd;
    [SerializeField] private float maxDistanceFromPath = 2f;

    private void Update()
    {
        Vector3 pathDirection = (pathEnd.position - pathStart.position).normalized;

        // Find closest point on the patrol path
        Vector3 closestPointOnPath = GetClosestPointOnRay(
            pathStart.position,
            pathDirection,
            transform.position
        );

        // Check if agent has strayed too far from the path
        float distanceFromPath = Vector3.Distance(transform.position, closestPointOnPath);

        if (distanceFromPath > maxDistanceFromPath)
        {
            Debug.Log("Agent has strayed from the path!");
            // Return to path logic here
        }
    }

    private Vector3 GetClosestPointOnRay(Vector3 rayOrigin, Vector3 rayDirection, Vector3 point)
    {
        float t = Vector3.Dot(point - rayOrigin, rayDirection);
        return rayOrigin + rayDirection * t;
    }
}
```

### Example 2: Rope/Cable Snap-to-Guide System

```csharp
public class CableGuideSystem : MonoBehaviour
{
    [SerializeField] private LineRenderer cableRenderer;
    [SerializeField] private Transform guideStart;
    [SerializeField] private Transform guideEnd;
    [SerializeField] private Transform cableEnd;
    [SerializeField] private float snapDistance = 1.5f;

    private void Update()
    {
        Vector3 guideDirection = (guideEnd.position - guideStart.position).normalized;

        // Find the closest point on the guide to the cable end
        Vector3 closestPoint = GetClosestPointOnRay(
            guideStart.position,
            guideDirection,
            cableEnd.position
        );

        float distance = Vector3.Distance(cableEnd.position, closestPoint);

        // Snap the cable if it's close enough to the guide
        Vector3 finalPosition = distance < snapDistance
            ? closestPoint
            : cableEnd.position;

        UpdateCableVisualization(finalPosition);
    }

    private void UpdateCableVisualization(Vector3 endPoint)
    {
        cableRenderer.SetPosition(0, transform.position);
        cableRenderer.SetPosition(1, endPoint);
    }

    private Vector3 GetClosestPointOnRay(Vector3 rayOrigin, Vector3 rayDirection, Vector3 point)
    {
        float t = Vector3.Dot(point - rayOrigin, rayDirection);
        return rayOrigin + rayDirection * t;
    }
}
```

### Example 3: Projectile Closest Approach Prediction

```csharp
public class ProjectileTracker : MonoBehaviour
{
    [SerializeField] private Transform target;
    [SerializeField] private float warningDistance = 5f;

    public void TrackProjectile(Vector3 projectilePosition, Vector3 projectileVelocity)
    {
        // Treat the projectile's trajectory as a ray
        Vector3 trajectoryDirection = projectileVelocity.normalized;

        // Find the closest point the projectile will get to the target
        Vector3 closestApproach = GetClosestPointOnRay(
            projectilePosition,
            trajectoryDirection,
            target.position
        );

        float closestDistance = Vector3.Distance(closestApproach, target.position);

        // Calculate time until closest approach
        float distanceToApproach = Vector3.Distance(projectilePosition, closestApproach);
        float timeToApproach = distanceToApproach / projectileVelocity.magnitude;

        if (closestDistance < warningDistance && timeToApproach > 0)
        {
            Debug.Log($"Warning! Projectile will pass within {closestDistance:F2}m in {timeToApproach:F2} seconds!");
            TriggerWarning();
        }
    }

    private void TriggerWarning()
    {
        // Activate warning UI or sound
    }

    private Vector3 GetClosestPointOnRay(Vector3 rayOrigin, Vector3 rayDirection, Vector3 point)
    {
        float t = Vector3.Dot(point - rayOrigin, rayDirection);
        return rayOrigin + rayDirection * t;
    }
}
```

### Example 4: Line Segment (Finite) Closest Point

```csharp
public class LineSegmentClosestPoint : MonoBehaviour
{
    public static Vector3 GetClosestPointOnLineSegment(
        Vector3 lineStart,
        Vector3 lineEnd,
        Vector3 point)
    {
        Vector3 lineDirection = lineEnd - lineStart;
        float lineLength = lineDirection.magnitude;
        lineDirection.Normalize();

        // Project onto the infinite ray
        float t = Vector3.Dot(point - lineStart, lineDirection);

        // Clamp t to the line segment bounds
        t = Mathf.Clamp(t, 0f, lineLength);

        // Calculate the closest point on the segment
        Vector3 closestPoint = lineStart + lineDirection * t;

        return closestPoint;
    }
}
```

### Example 5: Visual Debug Tool for Editor

```csharp
public class RayProximityVisualizer : MonoBehaviour
{
    [SerializeField] private Transform rayOrigin;
    [SerializeField] private Vector3 rayDirection = Vector3.forward;
    [SerializeField] private Transform testPoint;
    [SerializeField] private float rayLength = 10f;

    private void OnDrawGizmos()
    {
        if (rayOrigin == null || testPoint == null) return;

        Vector3 normalizedDirection = rayDirection.normalized;

        // Draw the ray
        Gizmos.color = Color.yellow;
        Gizmos.DrawLine(rayOrigin.position, rayOrigin.position + normalizedDirection * rayLength);

        // Calculate closest point
        Vector3 closestPoint = GetClosestPointOnRay(
            rayOrigin.position,
            normalizedDirection,
            testPoint.position
        );

        // Draw the connection
        Gizmos.color = Color.green;
        Gizmos.DrawSphere(closestPoint, 0.2f);

        Gizmos.color = Color.red;
        Gizmos.DrawLine(testPoint.position, closestPoint);

        // Draw distance label in Scene view
        UnityEditor.Handles.Label(
            closestPoint,
            $"Distance: {Vector3.Distance(testPoint.position, closestPoint):F2}m"
        );
    }

    private Vector3 GetClosestPointOnRay(Vector3 rayOrigin, Vector3 rayDirection, Vector3 point)
    {
        float t = Vector3.Dot(point - rayOrigin, rayDirection);
        return rayOrigin + rayDirection * t;
    }
}
```

## Best Practices

1. **Always Normalize Ray Direction**: Ensure your ray direction vector is normalized before using it in the calculation. This makes the `t` value represent actual distance along the ray and prevents unexpected scaling issues.

2. **Consider Line Segments vs Infinite Rays**: In most practical scenarios, you're working with line segments (finite) rather than infinite rays. Clamp the `t` value between 0 and the line length to prevent results beyond your intended boundaries.

3. **Cache Repeated Calculations**: If you're checking multiple points against the same ray, calculate the ray direction once and reuse it rather than recalculating for each point.

4. **Use for Early Rejection**: This technique is excellent for optimization. You can quickly determine if a point is close enough to a ray to warrant more expensive calculations like detailed collision detection.

5. **Combine with Distance Checks**: Always follow up the closest point calculation with a distance check to determine if the point is within your acceptable threshold. The closest point alone doesn't tell you if it's "close enough."

6. **Handle Edge Cases**: Check for zero-length rays or degenerate cases where the ray origin and direction might create numerical instability.

7. **Visualize During Development**: Use Unity's Gizmos to draw the ray, the test point, the closest point, and the connecting line. This visual feedback is invaluable for debugging spatial algorithms.

## Common Patterns

### Pattern 1: Bounded Ray with Min/Max Constraints

```csharp
public static Vector3 GetClosestPointOnBoundedRay(
    Vector3 rayOrigin,
    Vector3 rayDirection,
    Vector3 point,
    float minDistance = 0f,
    float maxDistance = Mathf.Infinity)
{
    float t = Vector3.Dot(point - rayOrigin, rayDirection);
    t = Mathf.Clamp(t, minDistance, maxDistance);
    return rayOrigin + rayDirection * t;
}
```

### Pattern 2: Closest Point with Direction Bias

```csharp
public static Vector3 GetClosestPointOnRayForward(
    Vector3 rayOrigin,
    Vector3 rayDirection,
    Vector3 point)
{
    float t = Vector3.Dot(point - rayOrigin, rayDirection);

    // Only consider points in front of the ray origin
    t = Mathf.Max(t, 0f);

    return rayOrigin + rayDirection * t;
}
```

### Pattern 3: Distance and Closest Point Combined

```csharp
public static Vector3 GetClosestPointOnRay(
    Vector3 rayOrigin,
    Vector3 rayDirection,
    Vector3 point,
    out float distance)
{
    float t = Vector3.Dot(point - rayOrigin, rayDirection);
    Vector3 closestPoint = rayOrigin + rayDirection * t;
    distance = Vector3.Distance(point, closestPoint);
    return closestPoint;
}
```

## Technical Details

### Vector Projection Mathematics

The technique relies on vector projection. When you have:
- Ray origin: **O**
- Ray direction (normalized): **D**
- Test point: **P**

The vector from origin to point is: **V = P - O**

The projection of **V** onto **D** gives you the scalar distance `t`:
```
t = V · D = (P - O) · D
```

This `t` value represents how far along the ray direction you need to travel from the origin to reach the perpendicular intersection point.

The closest point is then: **C = O + t * D**

### Why the Dot Product Works

The dot product `Vector3.Dot(V, D)` geometrically represents the length of the projection of vector **V** onto direction **D** (when **D** is normalized). This gives you the signed distance along the ray:
- Positive `t`: Point projects forward along the ray
- Negative `t`: Point projects backward from the ray origin
- Zero `t`: Point is perpendicular to the ray at its origin

### Performance Considerations

This calculation is extremely efficient:
- **Time Complexity**: O(1) - constant time
- **Operations**:
  - 1 vector subtraction
  - 1 dot product (3 multiplications + 2 additions)
  - 1 scalar multiplication
  - 1 vector addition

Compare this to iterative sampling methods which require O(n) operations where n is the number of samples, and you can see why understanding this mathematical approach is valuable.

## Conclusion

Calculating the closest point on a ray to a given point is a fundamental geometric operation that empowers you to solve numerous spatial problems efficiently. By leveraging vector projection through the dot product, you can implement AI pathfinding, cable physics, projectile tracking, and snap-to-line mechanics with minimal computational overhead.

The beauty of this technique lies in its simplicity and versatility. Once you understand the underlying mathematics, you'll find applications for it throughout your game development work. Whether you're building complex navigation systems, implementing physics simulations, or creating editor tools, this mathematical foundation proves invaluable.

Master this technique, and you'll have a powerful tool for solving spatial reasoning challenges with elegant, performant code.

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*
