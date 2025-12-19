import asyncio
import nats
from nats.js.api import StreamConfig, RetentionPolicy, StorageType


async def create_streams():
    print("🚀 Creating NATS streams...")

    nc = await nats.connect("nats://localhost:4222")
    js = nc.jetstream()

    taskiq_stream_config = StreamConfig(
        name="TASKIQ_STREAM",
        subjects=["taskiq.>"],
        retention=RetentionPolicy.WORK_QUEUE,
        max_msgs=100000,
        max_bytes=536870912,
        max_age=24 * 60 * 60,
        storage=StorageType.FILE,
        num_replicas=1,
    )

    eventbus_stream_config = StreamConfig(
        name="USERS_EVENTS",
        subjects=["users.events.>"],
        retention=RetentionPolicy.LIMITS,
        max_msgs=1000000,
        max_bytes=1073741824,
        max_age=7 * 24 * 60 * 60,
        storage=StorageType.FILE,
        num_replicas=1,
    )

    streams_to_create = [
        ("TASKIQ_STREAM", taskiq_stream_config),
        ("USERS_EVENTS", eventbus_stream_config),
    ]

    for stream_name, config in streams_to_create:
        try:
            stream = await js.add_stream(config)
            print(f"✅ Stream '{stream_name}' created")
            print(f"   Subjects: {stream.config.subjects}")
        except Exception as e:
            if "stream name already in use" in str(e):
                print(f"ℹ️ Stream '{stream_name}' already exists")
            else:
                print(f"❌ Failed to create '{stream_name}': {e}")

    print("\n📊 All streams:")
    streams = await js.streams_info()
    for stream in streams:
        print(f"  - {stream.config.name}")
        print(f"    Subjects: {stream.config.subjects}")
        print(f"    Messages: {stream.state.messages}")

    await nc.close()
    print("\n✅ Stream creation complete!")


if __name__ == "__main__":
    asyncio.run(create_streams())
