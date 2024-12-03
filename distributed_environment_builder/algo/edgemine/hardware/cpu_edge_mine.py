from distributed_environment_builder.infrastructure.hii.cpu_hii import CpuInstruction


class EdgeMineCpu:

    def __init__(self, cpu: CpuInstruction):
        self.cpu = cpu
