"""
Tests for ClientTools custom event loop functionality.
"""

import asyncio
import pytest
from elevenlabs.conversational_ai.conversation import ClientTools


class TestClientTools:
    """Test suite for ClientTools functionality."""
    
    def test_default_initialization(self):
        """Test that ClientTools can be initialized without parameters (backwards compatibility)."""
        client_tools = ClientTools()
        assert client_tools._custom_loop is None
        assert client_tools._loop is None
        assert not client_tools._running.is_set()
        
    def test_custom_loop_initialization(self):
        """Test that ClientTools can be initialized with a custom event loop."""
        loop = asyncio.new_event_loop()
        try:
            client_tools = ClientTools(loop=loop)
            assert client_tools._custom_loop is loop
            assert client_tools._loop is None
            assert not client_tools._running.is_set()
        finally:
            loop.close()
    
    def test_start_with_default_loop(self):
        """Test starting ClientTools with default behavior (creates own loop)."""
        client_tools = ClientTools()
        
        try:
            client_tools.start()
            assert client_tools._running.is_set()
            assert client_tools._loop is not None
            assert client_tools._thread is not None
            assert client_tools._thread.is_alive()
        finally:
            client_tools.stop()
    
    @pytest.mark.asyncio
    async def test_start_with_custom_loop(self):
        """Test starting ClientTools with a custom event loop."""
        custom_loop = asyncio.get_running_loop()
        client_tools = ClientTools(loop=custom_loop)
        
        try:
            client_tools.start()
            assert client_tools._running.is_set()
            assert client_tools._loop is custom_loop
            assert client_tools._thread is None  # No thread created for custom loop
        finally:
            client_tools.stop()
    
    def test_tool_registration(self):
        """Test that tools can be registered correctly."""
        client_tools = ClientTools()
        
        def sync_tool(params):
            return "sync result"
        
        async def async_tool(params):
            return "async result"
        
        client_tools.register("sync_tool", sync_tool, is_async=False)
        client_tools.register("async_tool", async_tool, is_async=True)
        
        assert "sync_tool" in client_tools.tools
        assert "async_tool" in client_tools.tools
        
        sync_handler, sync_is_async = client_tools.tools["sync_tool"]
        async_handler, async_is_async = client_tools.tools["async_tool"]
        
        assert sync_handler is sync_tool
        assert not sync_is_async
        assert async_handler is async_tool
        assert async_is_async
    
    def test_duplicate_tool_registration(self):
        """Test that registering a tool with the same name raises an error."""
        client_tools = ClientTools()
        
        def tool(params):
            return "result"
        
        client_tools.register("test_tool", tool)
        
        with pytest.raises(ValueError, match="Tool 'test_tool' is already registered"):
            client_tools.register("test_tool", tool)
    
    def test_invalid_handler_registration(self):
        """Test that registering a non-callable handler raises an error."""
        client_tools = ClientTools()
        
        with pytest.raises(ValueError, match="Handler must be callable"):
            client_tools.register("invalid_tool", "not_callable")
    
    @pytest.mark.asyncio
    async def test_sync_tool_execution_with_custom_loop(self):
        """Test executing a sync tool with a custom event loop."""
        custom_loop = asyncio.get_running_loop()
        client_tools = ClientTools(loop=custom_loop)
        
        def sync_tool(params):
            return f"sync result: {params.get('input', 'default')}"
        
        client_tools.register("sync_tool", sync_tool, is_async=False)
        client_tools.start()
        
        try:
            result = await client_tools.handle("sync_tool", {"input": "test"})
            assert result == "sync result: test"
        finally:
            client_tools.stop()
    
    @pytest.mark.asyncio
    async def test_async_tool_execution_with_custom_loop(self):
        """Test executing an async tool with a custom event loop."""
        custom_loop = asyncio.get_running_loop()
        client_tools = ClientTools(loop=custom_loop)
        
        async def async_tool(params):
            await asyncio.sleep(0.01)  # Simulate async work
            return f"async result: {params.get('input', 'default')}"
        
        client_tools.register("async_tool", async_tool, is_async=True)
        client_tools.start()
        
        try:
            result = await client_tools.handle("async_tool", {"input": "test"})
            assert result == "async result: test"
        finally:
            client_tools.stop()
    
    @pytest.mark.asyncio
    async def test_tool_execution_with_callback_custom_loop(self):
        """Test executing a tool via callback mechanism with custom event loop."""
        custom_loop = asyncio.get_running_loop()
        client_tools = ClientTools(loop=custom_loop)
        
        def sync_tool(params):
            return f"callback result: {params.get('data', 'none')}"
        
        client_tools.register("callback_tool", sync_tool, is_async=False)
        client_tools.start()
        
        callback_results = []
        
        def test_callback(response):
            callback_results.append(response)
        
        try:
            client_tools.execute_tool(
                "callback_tool", 
                {"tool_call_id": "test123", "data": "callback_test"}, 
                test_callback
            )
            
            # Wait for callback to be executed
            await asyncio.sleep(0.1)
            
            assert len(callback_results) == 1
            response = callback_results[0]
            assert response["type"] == "client_tool_result"
            assert response["tool_call_id"] == "test123"
            assert "callback result: callback_test" in response["result"]
            assert response["is_error"] is False
        finally:
            client_tools.stop()
    
    def test_sync_tool_execution_with_default_loop(self):
        """Test executing a sync tool with default loop behavior."""
        client_tools = ClientTools()
        
        def sync_tool(params):
            return f"default sync: {params.get('value', 'empty')}"
        
        client_tools.register("sync_tool", sync_tool, is_async=False)
        client_tools.start()
        
        # Use asyncio.run to test from a fresh event loop
        async def test():
            result = await client_tools.handle("sync_tool", {"value": "default_test"})
            return result
        
        try:
            result = asyncio.run(test())
            assert result == "default sync: default_test"
        finally:
            client_tools.stop()
    
    @pytest.mark.asyncio
    async def test_unregistered_tool_error(self):
        """Test that calling an unregistered tool raises an error."""
        custom_loop = asyncio.get_running_loop()
        client_tools = ClientTools(loop=custom_loop)
        client_tools.start()
        
        try:
            with pytest.raises(ValueError, match="Tool 'nonexistent' is not registered"):
                await client_tools.handle("nonexistent", {})
        finally:
            client_tools.stop()
    
    def test_execute_tool_without_start(self):
        """Test that execute_tool raises error when not started."""
        client_tools = ClientTools()
        
        def callback(response):
            pass
        
        with pytest.raises(RuntimeError, match="ClientTools event loop is not running"):
            client_tools.execute_tool("any_tool", {}, callback)
    
    @pytest.mark.asyncio
    async def test_tool_exception_handling(self):
        """Test that tool exceptions are handled correctly."""
        custom_loop = asyncio.get_running_loop()
        client_tools = ClientTools(loop=custom_loop)
        
        def failing_tool(params):
            raise ValueError("Tool failed intentionally")
        
        client_tools.register("failing_tool", failing_tool, is_async=False)
        client_tools.start()
        
        callback_results = []
        
        def error_callback(response):
            callback_results.append(response)
        
        try:
            client_tools.execute_tool(
                "failing_tool",
                {"tool_call_id": "error_test"},
                error_callback
            )
            
            # Wait for callback
            await asyncio.sleep(0.1)
            
            assert len(callback_results) == 1
            response = callback_results[0]
            assert response["type"] == "client_tool_result"
            assert response["tool_call_id"] == "error_test"
            assert response["is_error"] is True
            assert "Tool failed intentionally" in response["result"]
        finally:
            client_tools.stop()
    
    @pytest.mark.asyncio
    async def test_event_loop_isolation(self):
        """Test that custom loop prevents 'different event loop' errors."""
        # This test simulates the scenario mentioned in the GitHub issue
        main_loop = asyncio.get_running_loop()
        
        # Create ClientTools with the current loop
        client_tools = ClientTools(loop=main_loop)
        
        async def loop_aware_tool(params):
            # This tool checks which loop it's running on
            current_loop = asyncio.get_running_loop()
            return f"Running on loop: {id(current_loop)}"
        
        client_tools.register("loop_tool", loop_aware_tool, is_async=True)
        client_tools.start()
        
        try:
            result = await client_tools.handle("loop_tool", {})
            # The result should indicate it's running on the same loop
            expected_loop_id = str(id(main_loop))
            assert expected_loop_id in result
        finally:
            client_tools.stop()
    
    def test_stop_custom_loop_behavior(self):
        """Test that stop() doesn't close custom loops."""
        custom_loop = asyncio.new_event_loop()
        client_tools = ClientTools(loop=custom_loop)
        
        try:
            client_tools.start()
            assert client_tools._running.is_set()
            
            client_tools.stop()
            assert not client_tools._running.is_set()
            
            # Custom loop should still be open and usable
            assert not custom_loop.is_closed()
        finally:
            custom_loop.close()
    
    def test_stop_default_loop_behavior(self):
        """Test that stop() properly cleans up default loops."""
        client_tools = ClientTools()
        
        client_tools.start()
        assert client_tools._running.is_set()
        assert client_tools._thread is not None
        thread = client_tools._thread
        
        client_tools.stop()
        assert not client_tools._running.is_set()
        
        # Wait for thread to finish
        thread.join(timeout=1.0)
        assert not thread.is_alive()