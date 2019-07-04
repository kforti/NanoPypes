from dagster import PipelineDefinition



class PipelineBuilder:
    def __init__(self, pipes, dependencies):
        self.pipes = pipes
        self.solids = []

    def get_pipeline(self):
        for pipe in self.pipes:
            self.solids.extend([solid for solid in pipe])





