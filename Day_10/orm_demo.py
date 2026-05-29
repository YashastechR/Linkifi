"""
SQLAlchemy ORM Basics
=====================
Install: pip install sqlalchemy psycopg2-binary
"""

from sqlalchemy import (
    create_engine, Column, Integer, String,
    Numeric, DateTime, ForeignKey, func, and_, or_
)
from sqlalchemy.orm import DeclarativeBase, relationship, Session
from datetime import datetime

# ── 1. ENGINE ─────────────────────────────────────────────────────────────────
DB_URL = "postgresql+psycopg2://postgres:Yashas%40123@localhost:5433/mydb"

engine = create_engine(
    DB_URL,
    echo=False,       # Set True to print all SQL statements (great for debugging)
    pool_size=5,      # connection pool
    max_overflow=10
)


# ── 2. DEFINE MODELS (ORM) ───────────────────────────────────────────────────
class Base(DeclarativeBase):
    pass


class Department(Base):
    __tablename__ = "departments"

    id   = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    # Relationship: one dept → many employees
    employees = relationship("Employee", back_populates="department")

    def __repr__(self):
        return f"<Department id={self.id} name={self.name!r}>"


class Employee(Base):
    __tablename__ = "orm_employees"

    id         = Column(Integer, primary_key=True, autoincrement=True)
    name       = Column(String(100), nullable=False)
    email      = Column(String(150), unique=True)
    salary     = Column(Numeric(10, 2))
    dept_id    = Column(Integer, ForeignKey("departments.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relationship: many employees → one dept
    department = relationship("Department", back_populates="employees")

    def __repr__(self):
        return f"<Employee id={self.id} name={self.name!r} salary={self.salary}>"


# Create all tables
Base.metadata.create_all(engine)
print("✅ Tables created via ORM.")


# ── 3. CRUD OPERATIONS ───────────────────────────────────────────────────────
def create_records():
    """CREATE — add new rows."""
    with Session(engine) as session:
        # Create departments
        eng = Department(name="Engineering")
        mkt = Department(name="Marketing")
        hr  = Department(name="HR")
        session.add_all([eng, mkt, hr])
        session.flush()   # assigns IDs without committing

        # Create employees linked to departments
        employees = [
            Employee(name="Alice Johnson", email="alice@co.com", salary=95000, dept_id=eng.id),
            Employee(name="Bob Smith",     email="bob@co.com",   salary=72000, dept_id=mkt.id),
            Employee(name="Carol White",   email="carol@co.com", salary=88000, dept_id=eng.id),
            Employee(name="David Lee",     email="david@co.com", salary=65000, dept_id=hr.id),
        ]
        session.add_all(employees)
        session.commit()
        print(f"✅ Created {len(employees)} employees.")


def read_records():
    """READ — various ways to query."""
    with Session(engine) as session:

        # Get all
        all_emps = session.query(Employee).all()
        print(f"\n📋 All employees ({len(all_emps)}):")
        for e in all_emps:
            print(f"  {e}")

        # Get by primary key
        emp = session.get(Employee, 1)
        print(f"\n🔑 Get by PK: {emp}")

        # Filter
        engineers = (
            session.query(Employee)
            .join(Department)
            .filter(Department.name == "Engineering")
            .all()
        )
        print(f"\n🔍 Engineers: {engineers}")

        # AND / OR conditions
        rich_or_hr = (
            session.query(Employee)
            .join(Department)
            .filter(
                or_(
                    Employee.salary > 90000,
                    Department.name == "HR"
                )
            )
            .all()
        )
        print(f"\n💰 Salary > 90k OR in HR: {rich_or_hr}")

        # Order + limit
        top2 = (
            session.query(Employee)
            .order_by(Employee.salary.desc())
            .limit(2)
            .all()
        )
        print(f"\n🏆 Top 2 salaries: {top2}")

        # Aggregates
        avg_salary = session.query(func.avg(Employee.salary)).scalar()
        print(f"\n📊 Average salary: ${avg_salary:,.2f}")


def update_records():
    """UPDATE — modify existing rows."""
    with Session(engine) as session:
        # Update single record
        emp = session.get(Employee, 1)
        if emp:
            old = emp.salary
            emp.salary = float(emp.salary) * 1.10   # 10% raise
            session.commit()
            print(f"✅ Updated emp#1 salary: ${old} → ${emp.salary}")

        # Bulk update
        updated = (
            session.query(Employee)
            .filter(Employee.salary < 70000)
            .update({"salary": Employee.salary * 1.05})  # 5% raise for lower paid
        )
        session.commit()
        print(f"✅ Bulk updated {updated} employees.")


def delete_records():
    """DELETE — remove rows."""
    with Session(engine) as session:
        emp = session.query(Employee).filter_by(name="David Lee").first()
        if emp:
            session.delete(emp)
            session.commit()
            print(f"🗑️  Deleted employee: {emp.name}")


# ── 4. QUERYING WITH ORM — advanced patterns ─────────────────────────────────
def advanced_queries():
    with Session(engine) as session:

        # JOIN with relationship — employees + their department name
        results = (
            session.query(Employee.name, Employee.salary, Department.name.label("dept"))
            .join(Department)
            .order_by(Department.name, Employee.salary.desc())
            .all()
        )
        print("\n── JOIN Query ─────────────────────────────")
        for name, salary, dept in results:
            print(f"  {dept:15} | {name:20} | ${salary:>10,.2f}")

        # GROUP BY — avg salary per department
        dept_stats = (
            session.query(
                Department.name,
                func.count(Employee.id).label("headcount"),
                func.avg(Employee.salary).label("avg_salary")
            )
            .join(Employee)
            .group_by(Department.name)
            .all()
        )
        print("\n── Department Stats ───────────────────────")
        for dept, count, avg in dept_stats:
            print(f"  {dept:15} | {count} employees | avg ${avg:,.2f}")


# ── MAIN ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    create_records()
    read_records()
    update_records()
    delete_records()
    advanced_queries()
