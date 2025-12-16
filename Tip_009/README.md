# #UNITY TIPS 009/100

## Continuous Collision Detection - Preventing Fast-Moving Objects from Tunneling

<img src="Tip0009.png" alt="Continuous Collision Detection" width="300" align="left" style="margin-right: 20px; margin-bottom: 20px;">

When developing physics-based games in Unity, one of the most frustrating issues you'll encounter is fast-moving objects passing through colliders without triggering collisions. This phenomenon, known as "tunneling" or "ghosting," occurs when an object moves so quickly between physics updates that it completely bypasses collision checks. A classic example is a high-speed projectile passing through a wall, or a rapidly moving character phasing through the ground.

Unity's Continuous Collision Detection (CCD) system solves this critical problem by checking for collisions along the object's entire movement path between physics updates, rather than just at discrete points in time. Understanding when and how to use CCD is essential for creating robust physics interactions in your games.

<br clear="left">

## The Problem: Discrete Collision Detection Limitations

Unity's default collision detection mode is **Discrete**. In this mode, the physics engine checks for collisions only at the object's position at the beginning and end of each physics timestep (typically 0.02 seconds at 50Hz). Here's what happens:

1. **Frame 1**: Object is at position A (before the wall)
2. **Physics Update**: Object moves with high velocity
3. **Frame 2**: Object is now at position B (beyond the wall)
4. **Result**: No collision detected because the object "teleported" through the wall

This becomes problematic when:
- Objects move faster than their collider size per physics frame
- Thin colliders (like walls or floors) are involved
- Precision is critical (bullets, projectiles, racing games)
- High-speed character movement occurs

## The Solution: Continuous Collision Detection

CCD solves tunneling by **sweeping** the collider along its trajectory between physics updates, checking for any intersections along the entire path. Unity provides several CCD modes, each with different performance and accuracy trade-offs:

- **Discrete**: Default mode, checks only at timestep boundaries
- **Continuous**: Prevents tunneling against static colliders (non-Rigidbody objects)
- **Continuous Dynamic**: Prevents tunneling against both static and dynamic Rigidbodies with CCD enabled
- **Continuous Speculative**: Uses speculative contacts for smoother, faster CCD (Unity 2018.3+)

## Code Examples

### Example 1: Basic CCD Setup for Projectiles

```csharp
using UnityEngine;

public class Projectile : MonoBehaviour
{
    private Rigidbody rb;

    [SerializeField] private float speed = 50f;

    void Start()
    {
        rb = GetComponent<Rigidbody>();

        // Enable Continuous CCD for fast-moving projectile
        rb.collisionDetectionMode = CollisionDetectionMode.Continuous;

        // Launch the projectile
        rb.velocity = transform.forward * speed;
    }
}
```

### Example 2: Dynamic CCD for Interacting Fast Objects

```csharp
using UnityEngine;

public class RacingCar : MonoBehaviour
{
    private Rigidbody rb;

    [SerializeField] private float maxSpeed = 100f;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();

        // Use Continuous Dynamic to collide with other moving objects
        rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
    }

    void FixedUpdate()
    {
        // High-speed movement that could cause tunneling
        if (rb.velocity.magnitude > maxSpeed * 0.5f)
        {
            // CCD ensures we don't tunnel through barriers or other cars
            rb.AddForce(transform.forward * maxSpeed);
        }
    }
}
```

### Example 3: Adaptive CCD Based on Velocity

```csharp
using UnityEngine;

public class AdaptiveCCD : MonoBehaviour
{
    private Rigidbody rb;

    [SerializeField] private float ccdThreshold = 10f;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    void FixedUpdate()
    {
        // Dynamically switch CCD mode based on current speed
        float currentSpeed = rb.velocity.magnitude;

        if (currentSpeed > ccdThreshold)
        {
            rb.collisionDetectionMode = CollisionDetectionMode.Continuous;
        }
        else
        {
            // Save performance when moving slowly
            rb.collisionDetectionMode = CollisionDetectionMode.Discrete;
        }
    }
}
```

### Example 4: Bullet System with CCD

```csharp
using UnityEngine;

public class Bullet : MonoBehaviour
{
    private Rigidbody rb;

    [SerializeField] private float bulletSpeed = 100f;
    [SerializeField] private float lifetime = 5f;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();

        // Essential for high-speed bullets
        rb.collisionDetectionMode = CollisionDetectionMode.Continuous;

        // Optimize physics settings for bullets
        rb.interpolation = RigidbodyInterpolation.None;
        rb.useGravity = false;
    }

    public void Fire(Vector3 direction)
    {
        rb.velocity = direction.normalized * bulletSpeed;
        Destroy(gameObject, lifetime);
    }

    void OnCollisionEnter(Collision collision)
    {
        // CCD ensures this is always called, even at high speeds
        Debug.Log($"Bullet hit: {collision.gameObject.name}");
        Destroy(gameObject);
    }
}
```

### Example 5: CCD Manager for Multiple Objects

```csharp
using UnityEngine;

public class CCDManager : MonoBehaviour
{
    public enum CCDProfile
    {
        Static,
        Slow,
        Fast,
        VeryFast
    }

    public static void ApplyCCDProfile(Rigidbody rb, CCDProfile profile)
    {
        switch (profile)
        {
            case CCDProfile.Static:
                rb.collisionDetectionMode = CollisionDetectionMode.Discrete;
                rb.interpolation = RigidbodyInterpolation.None;
                break;

            case CCDProfile.Slow:
                rb.collisionDetectionMode = CollisionDetectionMode.Discrete;
                rb.interpolation = RigidbodyInterpolation.Interpolate;
                break;

            case CCDProfile.Fast:
                rb.collisionDetectionMode = CollisionDetectionMode.Continuous;
                rb.interpolation = RigidbodyInterpolation.Interpolate;
                break;

            case CCDProfile.VeryFast:
                rb.collisionDetectionMode = CollisionDetectionMode.ContinuousDynamic;
                rb.interpolation = RigidbodyInterpolation.Interpolate;
                break;
        }
    }
}

// Usage
public class SpaceShip : MonoBehaviour
{
    void Start()
    {
        Rigidbody rb = GetComponent<Rigidbody>();
        CCDManager.ApplyCCDProfile(rb, CCDManager.CCDProfile.Fast);
    }
}
```

### Example 6: Continuous Speculative for Kinematic Objects

```csharp
using UnityEngine;

public class MovingPlatform : MonoBehaviour
{
    private Rigidbody rb;

    [SerializeField] private Vector3 moveDistance = new Vector3(5f, 0f, 0f);
    [SerializeField] private float moveSpeed = 2f;

    private Vector3 startPos;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();
        rb.isKinematic = true;

        // Continuous Speculative is best for fast-moving kinematic objects
        rb.collisionDetectionMode = CollisionDetectionMode.ContinuousSpeculative;

        startPos = transform.position;
    }

    void FixedUpdate()
    {
        // Move platform back and forth
        float offset = Mathf.PingPong(Time.time * moveSpeed, 1f);
        Vector3 newPos = startPos + moveDistance * offset;

        // CCD ensures objects on platform don't fall through
        rb.MovePosition(newPos);
    }
}
```

## Best Practices

1. **Use CCD Selectively**: Only enable CCD on fast-moving objects where tunneling is a real risk. Every object with CCD enabled increases physics computation cost.

2. **Match CCD Modes to Use Cases**:
   - **Discrete**: Slow-moving or static objects, performance-critical scenarios
   - **Continuous**: Projectiles, fast players against static geometry
   - **Continuous Dynamic**: Racing games, objects that interact with other fast-moving objects
   - **Continuous Speculative**: Fast kinematic objects, moving platforms

3. **Consider the Velocity Threshold**: An object typically needs CCD when it moves faster than half its collider size per physics frame. Calculate this: `speed * Time.fixedDeltaTime > colliderSize * 0.5f`

4. **Combine with Appropriate Collider Shapes**: CCD works best with primitive colliders (Box, Sphere, Capsule). Mesh colliders with CCD are extremely expensive and should be avoided.

5. **Optimize Physics Settings Together**: CCD is most effective when paired with proper interpolation, appropriate fixed timestep values, and reasonable mass/velocity limits.

6. **Mind the Performance Impact**: CCD uses swept collision tests which are 2-10x more expensive than discrete checks. Profile your game and use CCD only where necessary.

7. **Test at Target Frame Rates**: Tunneling issues may only appear at certain frame rates or during lag spikes. Test CCD effectiveness under various performance conditions.

## Common Patterns

### Pattern 1: Speed-Based CCD Activation

Instead of always using CCD, activate it dynamically when objects exceed velocity thresholds:

```csharp
void FixedUpdate()
{
    float speed = rb.velocity.magnitude;
    float sizeThreshold = GetComponent<Collider>().bounds.size.magnitude * 0.5f;
    float velocityThreshold = sizeThreshold / Time.fixedDeltaTime;

    rb.collisionDetectionMode = speed > velocityThreshold
        ? CollisionDetectionMode.Continuous
        : CollisionDetectionMode.Discrete;
}
```

### Pattern 2: Layered Physics with CCD

Organize your physics objects into layers and apply CCD strategically:

```csharp
// Fast Layer: Bullets, projectiles → Continuous
// Dynamic Layer: Players, enemies → Continuous Dynamic
// Static Layer: Walls, floors → Discrete
// Slow Layer: Pickups, debris → Discrete
```

### Pattern 3: Pooled Objects with CCD

When using object pooling, ensure CCD settings are reset properly:

```csharp
public class PooledProjectile : MonoBehaviour
{
    private Rigidbody rb;

    void Awake()
    {
        rb = GetComponent<Rigidbody>();
    }

    void OnEnable()
    {
        // Reset CCD when object is reactivated from pool
        rb.collisionDetectionMode = CollisionDetectionMode.Continuous;
        rb.velocity = Vector3.zero;
    }
}
```

## Technical Details: How CCD Works

Continuous Collision Detection uses a technique called **conservative advancement** or **swept shape testing**:

1. **Sweep Volume**: The physics engine creates a swept volume representing all positions the collider occupies during the timestep
2. **Ray/Shape Casting**: It performs shape casts along the movement trajectory
3. **Time of Impact (TOI)**: Calculates the exact moment of first contact
4. **Collision Resolution**: Resolves the collision at the TOI, preventing interpenetration

**Continuous Speculative** uses a different approach:
- Predicts future contacts based on current velocity
- Generates speculative contact points ahead of time
- Generally faster but may miss very thin or fast-rotating colliders

**Performance Characteristics**:
- Discrete: ~1x cost (baseline)
- Continuous: ~2-5x cost
- Continuous Dynamic: ~5-10x cost
- Continuous Speculative: ~1.5-3x cost

The actual performance impact depends on scene complexity, collider types, and the number of CCD-enabled objects.

## When to Use Each Mode

| Scenario | Recommended Mode | Reason |
|----------|-----------------|---------|
| Slow-moving objects | Discrete | No tunneling risk, best performance |
| Fast bullets/projectiles | Continuous | Prevents tunneling through walls |
| Racing cars | Continuous Dynamic | Collides accurately with other cars |
| Moving platforms | Continuous Speculative | Smooth kinematic movement |
| Player character (normal speed) | Discrete | Usually moves slowly enough |
| Player character (dash/boost) | Continuous (when boosting) | Prevents wall clipping |

## Conclusion

Continuous Collision Detection is a powerful tool for ensuring reliable physics interactions in Unity, particularly for fast-moving objects. While discrete collision detection works well for most scenarios, understanding when and how to apply CCD can mean the difference between frustrating tunneling bugs and smooth, predictable physics behavior.

The key is finding the right balance: use CCD where it's needed to prevent tunneling, but avoid applying it universally to maintain good performance. By selectively enabling CCD based on object velocity, interaction requirements, and gameplay context, you can create robust physics systems that feel responsive and accurate without sacrificing frame rate.

Master CCD, and you'll build physics interactions that players can trust, whether they're firing high-speed projectiles, racing at breakneck speeds, or simply ensuring their character doesn't fall through the world during a lag spike.

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*
