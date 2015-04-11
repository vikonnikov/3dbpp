class DomainPair:
    """Structure for a domain pair in constraint programming
      int i;                 /* index of box i                        */
      int j;                 /* index of box j                        */
      int relation;          /* relation between the two boxes        */
      boolean domain;        /* domain of the two boxes               */
    """
    def __init__(self, i, j, relation, domain):
        self.i = i
        self.j = j

        self.update(relation, domain)

    def update(self, relation, domain):
        self.relation = relation
        self.domain = domain
    
    def __repr__(self):
        return 'DomainPair [%s][%s] Rel: %s Domain: %s' % \
            (self.i, self.j, self.relation, self.domain)

class TaskInfo:
    W = H = D = 10
    def __init__(self, boxes):
        self.n = len(boxes)
        print 'Length:', self.n