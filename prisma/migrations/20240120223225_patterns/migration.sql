/*
  Warnings:

  - The primary key for the `patterns` table will be changed. If it partially fails, the table could be left without primary key constraint.
  - You are about to drop the column `patternId` on the `patterns` table. All the data in the column will be lost.

*/
-- AlterTable
ALTER TABLE "patterns" DROP CONSTRAINT "patterns_pkey",
DROP COLUMN "patternId";

-- CreateTable
CREATE TABLE "users" (
    "login" TEXT NOT NULL,
    "firstName" TEXT NOT NULL,
    "lastName" TEXT NOT NULL,
    "Email" TEXT NOT NULL
);

-- CreateIndex
CREATE UNIQUE INDEX "users_login_key" ON "users"("login");

-- CreateIndex
CREATE UNIQUE INDEX "users_Email_key" ON "users"("Email");
