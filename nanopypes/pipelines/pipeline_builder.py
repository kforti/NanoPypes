from prefect import Flow


class PipelineBuilder:

    def __init__(self, pipeline_data, pipeline_order, pipeline_name):
        self.pipeline_order = pipeline_order
        self._pipeline = Flow(name=pipeline_name)
        self.pipeline_data = pipeline_data

    @property
    def pipeline(self):
        return self._pipeline

    def build_pipeline(self):
        for tool, command in self.pipeline_order:
            print(tool, command)
            self.pipeline_data.load_transform(tool, command)
            self._pipeline = self.pipeline_data.partition_data(self._pipeline)
            #self._pipeline = self.pipeline_data.build_commands(self._pipeline)
            #self._pipeline = self.pipeline_data.pipe_data(self._pipeline)

        #self._pipeline = self.pipeline_data.merge_data(self._pipeline, merge=True)



