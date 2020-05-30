from utils import printf

class DbDisplay():
    def __init__(self,rows=[],cols=[], rename={}):
        self.rows = rows
        self.cols = cols

    def padstr(self,fl, val):
        vstr = str(val).strip()
        n = len(vstr)
        pad = fl-n
        return " "*pad + vstr


    def get_col_lens(self):
        cols = self.cols
        rows = self.rows
        if len(cols) <= 0:
            cols = self.get_default_cols_names()
        if rows is None or len(rows) <=0:
            return {}
        clm = {}
        for col in cols:
            if col not in clm:
                clm[col] = len(str(col).strip())
        for r in rows:
            for c in cols:
                v = getattr(r, c, None)
                if v is None:
                    v = str(None)
                else:
                    v = str(v).strip()
                n = len(v)
                if clm[c] < n:
                    clm[c] = n
        return clm

    def get_default_col_names(self):
        rows = self.rows
        if rows is None or len(rows) <=0:
            return []
        return list(rows[1].__class__.__table__.columns.keys())

    def display(self):
        cols = self.cols
        rows = self.rows
        clm = self.get_col_lens()
        if len(cols) ==0:
            cols = self.get_default_col_names()
        out = []
        if len(rows) <= 0:
            return "Empty set\n"
        for col in cols:
            out.append(self.padstr(clm[col],col) + " ")
        out.append("\n")
        for row in rows:
            for col in cols:
                val = getattr(row, col)
                strval = str(val)
                out.append(self.padstr(clm[col], strval) + " ")
            out.append("\n")
        return "".join(out)
