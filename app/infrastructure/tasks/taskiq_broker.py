import asyncio
import logging
from taskiq_nats import NatsBroker
import nats
from nats.js.api import StreamConfig, RetentionPolicy, StorageType

logger = logging.getLogger(__name__)

_broker_instance = None


async def create_taskiq_stream():
    logger.info("Creating Taskiq stream...")

    try:
        nc = await nats.connect("nats://localhost:4222")
        js = nc.jetstream()

        stream_config = StreamConfig(
            name="TASKIQ_STREAM",
            subjects=["taskiq.>"],
            retention=RetentionPolicy.WORK_QUEUE,
            max_msgs=100000,
            max_bytes=536870912,
            max_age=24 * 60 * 60,
            storage=StorageType.FILE,
            num_replicas=1,
            duplicate_window=120,
        )

        try:
            stream = await js.add_stream(stream_config)
            logger.info(f"Taskiq stream created: {stream.config.name}")
            logger.info(f"   Subjects: {stream.config.subjects}")

        except Exception as e:
            if "stream name already in use" in str(e):
                logger.info("Taskiq stream already exists")
            else:
                logger.error(f"Failed to create Taskiq stream: {e}")
                raise

        await nc.close()

    except Exception as e:
        logger.error(f"Stream creation error: {e}")
        raise


def get_taskiq_broker() -> NatsBroker:
    global _broker_instance

    if _broker_instance is None:
        logger.info("Initializing Taskiq broker...")

        try:
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    asyncio.create_task(create_taskiq_stream())
                else:
                    asyncio.run(create_taskiq_stream())
            except RuntimeError:
                logger.warning("No event loop, stream will be created later")

            _broker_instance = NatsBroker(
                servers="nats://localhost:4222",
                queue="user_service",
            )

            logger.info("Taskiq broker created")
            logger.info("Queue: user_service")
            logger.info("Full subject: taskiq.user_service")

        except Exception as e:
            logger.error(f"Failed to create Taskiq broker: {e}")
            raise

    return _broker_instance


async def startup_broker():
    await create_taskiq_stream()

    broker = get_taskiq_broker()
    await broker.startup()
    logger.info("Broker started with stream")


async def shutdown_broker():
    global _broker_instance

    if _broker_instance is not None:
        await _broker_instance.shutdown()
        _broker_instance = None
        logger.info("Broker shutdown")


def get_broker():
    return get_taskiq_broker()
