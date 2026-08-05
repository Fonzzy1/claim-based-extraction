import numpy as np
from models.base_model import BaseLabelClass, Corpus

# a.M_net @ a.S_net
# a.E_net


class Analysis:
    def __init__(self, corpus: Corpus,) -> None:
        self.corpus = corpus
        self.issues = corpus.issues
        self.policies = corpus.policies

        self.issue_to_idx = {issue: i for i, issue in enumerate(self.issues)}
        self.policy_to_idx = {policy: i for i, policy in enumerate(self.policies)}

        self.S_pos = np.zeros(len(self.issues), dtype=int)
        self.S_neg = np.zeros(len(self.issues), dtype=int)

        self.E_pos = np.zeros(len(self.policies), dtype=int)
        self.E_neg = np.zeros(len(self.policies), dtype=int)

        self.M_pos = np.zeros((len(self.policies), len(self.issues)), dtype=int)
        self.M_neg = np.zeros((len(self.policies), len(self.issues)), dtype=int)

        self._build()

    def _build(self) -> None:
        for document in self.corpus.documents:
            if not document.elements:
                continue

            for element in document.elements:
                if not element.claims:
                    continue

                for claim in element.claims:
                    if isinstance(claim, dict):
                        claim = BaseLabelClass(**claim)

                    if claim.claim_type == "signal":
                        issue_idx = self.issue_to_idx[claim.issue]
                        if claim.label == 1:
                            self.S_pos[issue_idx] += 1
                        else:
                            self.S_neg[issue_idx] += 1

                    elif claim.claim_type == "evaluation":
                        policy_idx = self.policy_to_idx[claim.policy]
                        if claim.label == 1:
                            self.E_pos[policy_idx] += 1
                        else:
                            self.E_neg[policy_idx] += 1

                    elif claim.claim_type == "impact":
                        policy_idx = self.policy_to_idx[claim.policy]
                        issue_idx = self.issue_to_idx[claim.issue]
                        if claim.label == 1:
                            self.M_pos[policy_idx, issue_idx] += 1
                        else:
                            self.M_neg[policy_idx, issue_idx] += 1

    @property
    def S_net(self):
        return self.S_pos - self.S_neg

    @property
    def S_gross(self):
        return self.S_pos + self.S_neg

    @property
    def E_net(self):
        return self.E_pos - self.E_neg

    @property
    def E_gross(self):
        return self.E_pos + self.E_neg

    @property
    def M_net(self):
        return self.M_pos - self.M_neg

    @property
    def M_gross(self):
        return self.M_pos + self.M_neg
