import collections
from typing import Optional, Type, Any, Tuple, List

from nodeflow.adapter.abstract import Adapter
from nodeflow.adapter.pipeline import Pipeline
from nodeflow.node.variable import Variable
from nodeflow.node.function import Function

class Converter:
    ROOT_CONVERTER: Optional['Converter'] = None

    def __init__(self, adapters=None, sub_converters=None):
        self.graph = collections.defaultdict(list)
        self.sub_converters = set()
        if adapters:
            self.register_adapters(adapters)
        if sub_converters:
            self.register_converters(sub_converters)

    def __enter__(self):
        Converter.ROOT_CONVERTER = self

    def __exit__(self, exc_type, exc_val, exc_tb):
        Converter.ROOT_CONVERTER = None

    def convert(self, variable, to_type) -> Optional[Variable]:
        pipeline, preserves_info = self.get_converting_pipeline(type(variable), to_type)
        if pipeline:
            return pipeline.compute(variable)
        return None

    def get_converting_pipeline(self, source, target) -> Tuple[Optional[Pipeline], bool]:
        # Find the shortest path in the graph
        visited = set()
        queue = collections.deque([(source, Pipeline(), False)])
        while queue:
            current_type, current_pipeline, loses_info = queue.popleft()
            if current_type == target:
                return current_pipeline, not loses_info
            if current_type in visited:
                continue
            visited.add(current_type)
            for adapter in self.graph[current_type]:
                new_pipeline = Pipeline()
                new_pipeline._pipeline = current_pipeline._pipeline + [adapter]
                new_pipeline._loose_information = current_pipeline._loose_information or adapter.is_loses_information()
                queue.append((adapter.get_type_of_target_variable(), new_pipeline, new_pipeline._loose_information))
        return None, False

    def is_support_variable(self, variable_type) -> bool:
        return variable_type in self.graph

    def register_adapter(self, adapter: Adapter):
        source_type = adapter.get_type_of_source_variable()
        self.graph[source_type].append(adapter)

    def register_adapters(self, adapters: List[Adapter]):
        for adapter in adapters:
            self.register_adapter(adapter)

    def register_converter(self, converter: 'Converter'):
        self.sub_converters.add(converter)

    def register_converters(self, converters: List['Converter']):
        for converter in converters:
            self.register_converter(converter)

BUILTIN_CONVERTER = Converter()
__all__ = ["Converter"]