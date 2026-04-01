#!/bin/bash

# ============================================================
#   HBNB Part 3 — Script de tests complet
#   Usage: bash test_hbnb.sh
# ============================================================

BASE_URL="http://127.0.0.1:5000/api/v1"
DB_PATH="$HOME/Holberton/holbertonschool-hbnb/part3/hbnb/instance/hbnb_dev.db"

PASS=0
FAIL=0

sep()  { echo ""; echo "────────────────────────────────────────"; echo "  $1"; echo "────────────────────────────────────────"; }
ok()   { echo "  ✅ OK  — $1"; PASS=$((PASS + 1)); }
no()   { echo "  ❌ NO  — $1"; echo "         > $2"; FAIL=$((FAIL + 1)); }

check() {
    local label="$1" response="$2" expected="$3" actual="$4" field="$5"
    local fail_reason=""
    if [ "$actual" != "$expected" ]; then
        fail_reason="HTTP $actual (attendu $expected)"
    elif [ -n "$field" ]; then
        local val
        val=$(echo "$response" | python3 -c "import sys,json; print(json.load(sys.stdin).get('$field','null'))" 2>/dev/null)
        if [ "$val" = "None" ] || [ "$val" = "null" ] || [ -z "$val" ]; then
            fail_reason="champ '$field' est null"
        fi
    fi
    [ -z "$fail_reason" ] && ok "$label" || no "$label" "$fail_reason"
}

# ── Verification Flask ────────────────────────────────────────

sep "Verification Flask"
if ! curl -s "$BASE_URL/places/" > /dev/null 2>&1; then
    echo "  ❌ Flask n'est pas demarre — lance : python3 run.py"
    exit 1
fi
ok "Flask demarre sur le port 5000"

# ── Setup ─────────────────────────────────────────────────────

sep "Setup — Connexion et creation des places"

ADMIN_BODY=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "admin@hbnb.io", "password": "Admin1234"}')
ADMIN_TOKEN=$(echo "$ADMIN_BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)
[ -n "$ADMIN_TOKEN" ] && ok "Login Admin" || no "Login Admin" "token absent"

JOHN_BODY=$(curl -s -X POST "$BASE_URL/auth/login" \
  -H "Content-Type: application/json" \
  -d '{"email": "john.doe@example.com", "password": "Password123"}')
JOHN_TOKEN=$(echo "$JOHN_BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('access_token',''))" 2>/dev/null)
[ -n "$JOHN_TOKEN" ] && ok "Login John Doe" || no "Login John Doe" "token absent"

AP_BODY=$(curl -s -X POST "$BASE_URL/places/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Lieu Admin Test", "price": 100.0, "latitude": 45.0, "longitude": 5.0}')
ADMIN_PLACE=$(echo "$AP_BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
[ -n "$ADMIN_PLACE" ] && ok "Place Admin creee" || no "Place Admin creee" "$(echo $AP_BODY | head -c 100)"

JP_BODY=$(curl -s -X POST "$BASE_URL/places/" \
  -H "Authorization: Bearer $JOHN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Lieu John Test", "price": 75.0, "latitude": 48.8566, "longitude": 2.3522}')
JOHN_PLACE=$(echo "$JP_BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
[ -n "$JOHN_PLACE" ] && ok "Place John creee" || no "Place John creee" "$(echo $JP_BODY | head -c 100)"

# ── TEST 1 ────────────────────────────────────────────────────

sep "TEST 1 — Creer un user"

RAND="$(python3 -c 'import uuid; print(uuid.uuid4().hex[:8])')"
R=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/users/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"first_name\": \"Test\", \"last_name\": \"User\", \"email\": \"test_${RAND}@example.com\", \"password\": \"Password123\"}")
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "POST /users/ retourne 201" "$BODY" "201" "$CODE"
echo "$BODY" | grep -q '"password"' \
  && no "password absent de la reponse" "le champ password est visible" \
  || ok "password absent de la reponse"

# ── TEST 2 ────────────────────────────────────────────────────

sep "TEST 2 — GET user sans password"

JOHN_ID="6aadb320-f58c-4967-8569-5926a7d8bc20"
R=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/users/$JOHN_ID")
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "GET /users/:id retourne 200" "$BODY" "200" "$CODE"
echo "$BODY" | grep -q '"password_hash"' \
  && no "password_hash absent de la reponse" "le champ password_hash est visible" \
  || ok "password_hash absent de la reponse"

# ── TEST 3 ────────────────────────────────────────────────────

sep "TEST 3 — Login et Token JWT"

[ -n "$JOHN_TOKEN" ] && ok "Token JWT recu apres login" || no "Token JWT recu" "token vide"

# ── TEST 4 ────────────────────────────────────────────────────

sep "TEST 4 — Endpoint protege"

R=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/auth/protected" -H "Authorization: Bearer $JOHN_TOKEN")
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "Acces avec token -> 200" "$BODY" "200" "$CODE"

R=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/auth/protected")
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "Acces sans token -> 401" "$BODY" "401" "$CODE"

# ── TEST 5 ────────────────────────────────────────────────────

sep "TEST 5 — Creer un lieu"

[ -n "$ADMIN_PLACE" ] && ok "Place creee (201) avec owner_id" || no "Place creee" "id absent"

# ── TEST 6 ────────────────────────────────────────────────────

sep "TEST 6 — Modifier le lieu de quelqu'un d'autre"

R=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/places/$ADMIN_PLACE" \
  -H "Authorization: Bearer $JOHN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"title": "Tentative"}')
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "John modifie place Admin -> 403" "$BODY" "403" "$CODE"

# ── TEST 7 ────────────────────────────────────────────────────

sep "TEST 7 — Creer un avis"

sqlite3 "$DB_PATH" "DELETE FROM reviews WHERE user_id='$JOHN_ID' AND place_id='$ADMIN_PLACE';" 2>/dev/null

R=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/reviews/" \
  -H "Authorization: Bearer $JOHN_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"place_id\": \"$ADMIN_PLACE\", \"text\": \"Super endroit\", \"rating\": 4}")
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
REVIEW_ID=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('id',''))" 2>/dev/null)
check "POST /reviews/ retourne 200" "$BODY" "200" "$CODE"

UID=$(echo "$BODY" | python3 -c "import sys,json; print(json.load(sys.stdin).get('user_id','null'))" 2>/dev/null)
[ "$UID" != "null" ] && [ -n "$UID" ] \
  && ok "user_id present et non null" \
  || no "user_id present et non null" "user_id est null"

# ── TEST 8 ────────────────────────────────────────────────────

sep "TEST 8 — Modifier un avis"

R=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $JOHN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text": "Avis mis a jour !"}')
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "PUT /reviews/:id retourne 200" "$BODY" "200" "$CODE" "text"

# ── TEST 9 ────────────────────────────────────────────────────

sep "TEST 9 — Supprimer un avis"

R=$(curl -s -w "\n%{http_code}" -X DELETE "$BASE_URL/reviews/$REVIEW_ID" \
  -H "Authorization: Bearer $JOHN_TOKEN")
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "DELETE /reviews/:id retourne 200" "$BODY" "200" "$CODE"

# ── TEST 10 ───────────────────────────────────────────────────

sep "TEST 10 — Modifier ses propres donnees"

R=$(curl -s -w "\n%{http_code}" -X PUT "$BASE_URL/users/$JOHN_ID" \
  -H "Authorization: Bearer $JOHN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"first_name": "Johnny"}')
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "PUT /users/:id (son propre compte) -> 200" "$BODY" "200" "$CODE"

# ── TEST 11 ───────────────────────────────────────────────────

sep "TEST 11 — Endpoints publics (sans token)"

R=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/places/")
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "GET /places/ sans token -> 200" "$BODY" "200" "$CODE"

R=$(curl -s -w "\n%{http_code}" -X GET "$BASE_URL/places/$ADMIN_PLACE")
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "GET /places/:id sans token -> 200" "$BODY" "200" "$CODE"

# ── TEST 12 ───────────────────────────────────────────────────

sep "TEST 12 — Endpoints admin (amenities)"

RAND2="$(python3 -c 'import uuid; print(uuid.uuid4().hex[:6])')"
R=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/amenities/" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"name\": \"Amenity_${RAND2}\"}")
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "POST /amenities/ (admin) -> 201" "$BODY" "201" "$CODE"

R=$(curl -s -w "\n%{http_code}" -X POST "$BASE_URL/amenities/" \
  -H "Authorization: Bearer $JOHN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name": "Tentative"}')
CODE=$(echo "$R" | tail -1); BODY=$(echo "$R" | head -n -1)
check "POST /amenities/ (non-admin) -> 403" "$BODY" "403" "$CODE"

# ── TEST 13 ───────────────────────────────────────────────────

sep "TEST 13 — CASCADE SQL"

CASCADE=$(sqlite3 "$DB_PATH" << 'EOF'
PRAGMA foreign_keys = ON;
INSERT OR IGNORE INTO users (id, first_name, last_name, email, password_hash, is_admin, created_at, updated_at)
VALUES ('testcasc-0000-0000-0000-000000000001', 'Casc', 'Test', 'casc@test.com', 'x', 0, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO places (id, title, price, owner_id, created_at, updated_at)
VALUES ('testcasc-0000-0000-0000-000000000002', 'CascPlace', 1.0, 'testcasc-0000-0000-0000-000000000001', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
INSERT OR IGNORE INTO reviews (id, text, rating, user_id, place_id, created_at, updated_at)
VALUES ('testcasc-0000-0000-0000-000000000003', 'CascReview', 3, 'testcasc-0000-0000-0000-000000000001', 'testcasc-0000-0000-0000-000000000002', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);
DELETE FROM places WHERE id = 'testcasc-0000-0000-0000-000000000002';
SELECT COUNT(*) FROM reviews WHERE place_id = 'testcasc-0000-0000-0000-000000000002';
DELETE FROM users WHERE id = 'testcasc-0000-0000-0000-000000000001';
SELECT COUNT(*) FROM places WHERE owner_id = 'testcasc-0000-0000-0000-000000000001';
SELECT COUNT(*) FROM reviews WHERE user_id = 'testcasc-0000-0000-0000-000000000001';
EOF
)

R1=$(echo "$CASCADE" | sed -n '1p')
R2=$(echo "$CASCADE" | sed -n '2p')
R3=$(echo "$CASCADE" | sed -n '3p')

[ "$R1" = "0" ] && ok "Supprimer un place -> ses reviews disparaissent" || no "Supprimer un place -> ses reviews disparaissent" "$R1 review(s) restant(s)"
[ "$R2" = "0" ] && ok "Supprimer un user -> ses places disparaissent"   || no "Supprimer un user -> ses places disparaissent"   "$R2 place(s) restant(s)"
[ "$R3" = "0" ] && ok "Supprimer un user -> ses reviews disparaissent"  || no "Supprimer un user -> ses reviews disparaissent"  "$R3 review(s) restant(s)"

# ── Resume ────────────────────────────────────────────────────

TOTAL=$((PASS + FAIL))
echo ""
echo "════════════════════════════════════════"
echo "  RESULTAT FINAL : $PASS / $TOTAL OK"
echo "════════════════════════════════════════"
if [ "$FAIL" -eq 0 ]; then
    echo "  ✅ Tout est OK — pret a rendre !"
else
    echo "  ❌ $FAIL test(s) ont echoue"
    echo "     Cherche les lignes NO ci-dessus"
fi
echo ""
