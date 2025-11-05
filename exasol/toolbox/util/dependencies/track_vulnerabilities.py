from pydantic import (
    BaseModel,
    ConfigDict,
)

from exasol.toolbox.util.dependencies.audit import Vulnerability


class ResolvedVulnerabilities(BaseModel):
    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    previous_vulnerabilities: list[Vulnerability]
    current_vulnerabilities: list[Vulnerability]

    def _is_resolved(self, previous_vuln: Vulnerability):
        """
        Detects if a vulnerability has been resolved.

        A vulnerability is said to be resolved when it cannot be found
        in the `current_vulnerabilities`. In order to see if a vulnerability
        is still present, its id and aliases are compared to values in the
        `current_vulnerabilities`. While one could hope that the IDs
        are the same, it's possible between pip-audit versions that
        there are differences.
        """
        previous_vuln_set = {previous_vuln.id, *previous_vuln.aliases}
        for current_vuln in self.current_vulnerabilities:
            if previous_vuln.name == current_vuln.name:
                current_vuln_id_set = {current_vuln.id, *current_vuln.aliases}
                if previous_vuln_set.intersection(current_vuln_id_set):
                    return False
        return True

    @property
    def resolutions(self) -> list[Vulnerability]:
        """
        Return resolved vulnerabilities
        """
        resolved_vulnerabilities = []
        for previous_vuln in self.previous_vulnerabilities:
            if self._is_resolved(previous_vuln):
                resolved_vulnerabilities.append(previous_vuln)
        return resolved_vulnerabilities
