# #UNITY TIPS 005/100

## Enabling Collisions Between Kinematic Rigidbodies and Static Colliders

Unity's physics system has specific rules about which objects can collide with each other. By default, a kinematic rigidbody won't generate collision events with static colliders (colliders without a rigidbody component). This can be confusing when you expect collisions to work but they simply don't trigger. Fortunately, Unity provides a project-level setting to enable this behavior.

## The Problem

In Unity's default physics configuration, collisions only occur between certain combinations of rigidbody types:

- **Dynamic Rigidbody ↔ Dynamic Rigidbody**: ✅ Collides
- **Dynamic Rigidbody ↔ Kinematic Rigidbody**: ✅ Collides
- **Dynamic Rigidbody ↔ Static Collider**: ✅ Collides
- **Kinematic Rigidbody ↔ Static Collider**: ❌ Does NOT collide (by default)

This default behavior is optimized for performance, assuming that kinematic objects (player-controlled characters, moving platforms) won't need to detect collisions with static geometry. However, many game scenarios require exactly this type of collision detection.

## The Solution: Enable Kinematic Static Pairs

Unity provides a project-wide setting called **"Enable Kinematic Static Pairs"** that allows kinematic rigidbodies to generate collision events with static colliders.

### How to Enable It

1. Open **Edit → Project Settings**
2. Navigate to the **Physics** section (or **Physics 2D** for 2D projects)
3. Find the **"Enable Enhanced Determinism"** section
4. Check the box for **"Enable Kinematic Static Pairs"**

Once enabled, your kinematic rigidbodies will now trigger `OnCollisionEnter`, `OnCollisionStay`, and `OnCollisionExit` events when interacting with static colliders.

## Code Examples

### Example 1: Basic Kinematic-Static Collision Detection

```csharp
using UnityEngine;

public class KinematicPlayer : MonoBehaviour
{
    private Rigidbody rb;

    private void Start()
    {
        rb = GetComponent<Rigidbody>();
        rb.isKinematic = true; // Make this a kinematic rigidbody
    }

    private void OnCollisionEnter(Collision collision)
    {
        // With "Enable Kinematic Static Pairs" enabled,
        // this will trigger even when hitting static colliders
        Debug.Log($"Kinematic player collided with: {collision.gameObject.name}");
    }
}
```

### Example 2: Custom Character Controller with Wall Detection

```csharp
using UnityEngine;

public class CustomCharacterController : MonoBehaviour
{
    private Rigidbody rb;
    private bool isTouchingWall = false;

    private void Start()
    {
        rb = GetComponent<Rigidbody>();
        rb.isKinematic = true;
    }

    private void Update()
    {
        // Move character using kinematic control
        Vector3 movement = new Vector3(Input.GetAxis("Horizontal"), 0, Input.GetAxis("Vertical"));
        rb.MovePosition(rb.position + movement * 5f * Time.deltaTime);
    }

    private void OnCollisionEnter(Collision collision)
    {
        // Detect walls (static colliders) for gameplay mechanics
        if (collision.gameObject.CompareTag("Wall"))
        {
            isTouchingWall = true;
            Debug.Log("Can now wall jump!");
        }
    }

    private void OnCollisionExit(Collision collision)
    {
        if (collision.gameObject.CompareTag("Wall"))
        {
            isTouchingWall = false;
        }
    }
}
```

### Example 3: Moving Platform Interaction Detection

```csharp
using UnityEngine;

public class MovingPlatform : MonoBehaviour
{
    private Rigidbody rb;
    private Vector3 startPos;
    private Vector3 endPos;
    private float speed = 2f;

    private void Start()
    {
        rb = GetComponent<Rigidbody>();
        rb.isKinematic = true;

        startPos = transform.position;
        endPos = startPos + new Vector3(10f, 0, 0);
    }

    private void FixedUpdate()
    {
        // Move platform kinematically
        float pingPong = Mathf.PingPong(Time.time * speed, 1f);
        Vector3 newPos = Vector3.Lerp(startPos, endPos, pingPong);
        rb.MovePosition(newPos);
    }

    private void OnCollisionEnter(Collision collision)
    {
        // Detect when the platform hits static obstacles
        if (collision.gameObject.CompareTag("Obstacle"))
        {
            Debug.Log("Platform encountered obstacle!");
            // Could reverse direction or stop
        }
    }
}
```

### Example 4: Projectile Impact Detection

```csharp
using UnityEngine;

public class KinematicProjectile : MonoBehaviour
{
    private Rigidbody rb;
    [SerializeField] private float speed = 20f;
    [SerializeField] private GameObject impactEffect;

    private void Start()
    {
        rb = GetComponent<Rigidbody>();
        rb.isKinematic = true;
    }

    private void FixedUpdate()
    {
        // Move projectile using kinematic physics for precise control
        rb.MovePosition(rb.position + transform.forward * speed * Time.fixedDeltaTime);
    }

    private void OnCollisionEnter(Collision collision)
    {
        // With kinematic-static pairs enabled, this detects
        // collisions with static environment geometry

        ContactPoint contact = collision.GetContact(0);

        // Spawn impact effect at collision point
        if (impactEffect != null)
        {
            Instantiate(impactEffect, contact.point, Quaternion.LookRotation(contact.normal));
        }

        Debug.Log($"Projectile hit: {collision.gameObject.name}");
        Destroy(gameObject);
    }
}
```

### Example 5: 2D Platform Game Implementation

```csharp
using UnityEngine;

public class Player2DController : MonoBehaviour
{
    private Rigidbody2D rb;
    [SerializeField] private float moveSpeed = 5f;
    [SerializeField] private float jumpForce = 10f;
    private bool isGrounded = false;

    private void Start()
    {
        rb = GetComponent<Rigidbody2D>();
        rb.bodyType = RigidbodyType2D.Kinematic;
    }

    private void Update()
    {
        // Horizontal movement
        float horizontal = Input.GetAxis("Horizontal");
        rb.velocity = new Vector2(horizontal * moveSpeed, rb.velocity.y);

        // Jump when grounded
        if (Input.GetButtonDown("Jump") && isGrounded)
        {
            // Temporarily switch to dynamic for jump
            rb.bodyType = RigidbodyType2D.Dynamic;
            rb.AddForce(Vector2.up * jumpForce, ForceMode2D.Impulse);
        }
    }

    private void OnCollisionEnter2D(Collision2D collision)
    {
        // Detect ground (static colliders) thanks to kinematic-static pairs
        if (collision.gameObject.CompareTag("Ground"))
        {
            isGrounded = true;
            rb.bodyType = RigidbodyType2D.Kinematic;
        }
    }

    private void OnCollisionExit2D(Collision2D collision)
    {
        if (collision.gameObject.CompareTag("Ground"))
        {
            isGrounded = false;
        }
    }
}
```

## Best Practices

1. **Understand the Performance Impact**: Enabling kinematic-static collision pairs adds computational overhead. The physics engine must now check for collisions that were previously skipped. Only enable this setting if your game requires it.

2. **Use Triggers for Detection When Possible**: If you only need to detect overlap without physical collision response, consider using trigger colliders (`OnTriggerEnter`). Triggers work between all object types and are more performant.

3. **Consider Alternative Approaches**: For simple ground detection, raycasting or sphere casting might be more efficient than relying on collision events.

4. **Apply Per-Scene Logic**: Since this is a project-wide setting, ensure all your scenes and game mechanics account for the enabled behavior. Document this choice in your project's technical documentation.

5. **Test Thoroughly After Enabling**: This setting changes fundamental physics behavior. Test all physics-related gameplay after enabling it to ensure nothing breaks unexpectedly.

6. **Combine with Collision Layers**: Use Unity's Layer Collision Matrix (Edit → Project Settings → Physics → Layer Collision Matrix) to fine-tune which specific layers should collide, optimizing performance while keeping the functionality you need.

7. **Profile Your Game**: Use the Unity Profiler to measure the performance impact of enabling kinematic-static pairs, especially in physics-heavy scenes with many objects.

## When to Use Kinematic-Static Collision Detection

### Good Use Cases:
- Custom character controllers that need to detect walls, floors, and obstacles
- Moving platforms that need to detect static obstacles in their path
- Kinematically-controlled projectiles that need to hit static environment geometry
- Puzzle games where kinematic objects must interact with static level elements
- Animation-driven objects that need collision feedback with the environment

### Consider Alternatives When:
- You only need simple ground detection (use raycasting instead)
- You're building a physics-based game with dynamic rigidbodies (use dynamic rigidbodies)
- Performance is critical and you have many kinematic objects (use triggers or raycasts)
- You need one-way platforms or ghost collisions (use trigger colliders with custom logic)

## Common Patterns

### Pattern 1: Hybrid Movement System

```csharp
// Switch between kinematic and dynamic based on context
if (playerControlled)
{
    rb.isKinematic = true; // Precise control
}
else
{
    rb.isKinematic = false; // Physics-driven (e.g., ragdoll)
}
```

### Pattern 2: Collision Layer Optimization

```csharp
// Use layers to control which kinematic-static pairs actually collide
// Set in Project Settings → Physics → Layer Collision Matrix
// Example: Enable "Player" (kinematic) vs "Environment" (static)
// Disable "Player" (kinematic) vs "Decoration" (static)
```

### Pattern 3: Conditional Collision Response

```csharp
private void OnCollisionEnter(Collision collision)
{
    // Only respond to specific static collider types
    if (collision.gameObject.layer == LayerMask.NameToLayer("Environment"))
    {
        HandleEnvironmentCollision(collision);
    }
}
```

## Technical Details

### How It Works

When "Enable Kinematic Static Pairs" is disabled (default), Unity's physics engine uses the following optimization:

```
if (object1.isKinematic && object2.isStatic) {
    skip_collision_check(); // Performance optimization
}
```

When enabled, the physics engine performs collision detection for these pairs:

```
if (object1.isKinematic && object2.isStatic) {
    perform_collision_detection(); // Now checks and triggers events
}
```

### Physics Configuration Locations

- **3D Physics**: Edit → Project Settings → Physics → Enable Kinematic Static Pairs
- **2D Physics**: Edit → Project Settings → Physics 2D → Enable Kinematic Static Pairs

These settings are independent, so you need to enable the appropriate one for your project type.

### Performance Considerations

The performance cost depends on:
- Number of kinematic rigidbodies in the scene
- Number of static colliders in the scene
- Complexity of collider shapes (mesh colliders are most expensive)
- Update frequency of kinematic objects

For most games, the performance impact is negligible, but physics-heavy mobile games should profile carefully.

## Conclusion

Enabling kinematic-static collision pairs unlocks powerful gameplay possibilities for custom character controllers, animated objects, and precise movement systems. While it adds a small performance cost, the ability to detect collisions between kinematic rigidbodies and static environment geometry is essential for many game mechanics.

By understanding when to use this setting and combining it with proper layer management and performance profiling, you can create responsive, physics-aware gameplay systems that give you precise control while still benefiting from Unity's collision detection system.

Remember: this is a project-wide setting that affects all physics calculations, so enable it intentionally and test thoroughly to ensure your game behaves as expected.

*Credits to Binary Impact GmbH for the developer card inspiring this write-up.*
